import asyncio
import json
import os
import time
from typing import Any, TypeVar

import aioconsole
import anthropic
import dotenv
import openai
import PIL.Image
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionContentPartImageParam,
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)

from skillweaver.util.image_to_base64 import image_to_base64, image_to_data_url
from skillweaver.util.perfmon import monitor

dotenv.load_dotenv()

Function = dict
NoArgs = object()

ResponseFormatT = TypeVar("ResponseFormatT")


async def completion_openai(
    client: openai.AsyncAzureOpenAI | openai.AsyncOpenAI,
    model: str,
    messages: list[ChatCompletionMessageParam],
    json_mode=False,
    json_schema=None,
    tools: list[Function] = [],
    args: dict = NoArgs,  # type: ignore
    key="general",
) -> Any:
    if args is NoArgs:
        args = {}
    else:
        args = {**args}

    tries = 5
    backoff = 4
    for i in range(tries):
        try:
            start_time = time.time()

            if json_mode:
                response_format = {"type": "json_object"}
            elif json_schema:
                response_format = {
                    "type": "json_schema",
                    "json_schema": json_schema,
                }
            else:
                response_format = {"type": "text"}

            response: ChatCompletion = await client.chat.completions.create(
                model=model,
                messages=messages,  # type: ignore
                response_format=response_format,  # type: ignore
                **(
                    {
                        "tools": tools,
                        "tool_choice": "required",
                        "parallel_tool_calls": False,
                    }
                    if len(tools) > 0
                    else {}
                ),
                **args,
            )

            end_time = time.time()
            monitor.log_timing_event("lm/" + key, start_time, end_time)
            assert response.usage
            msg = response.choices[0].message
            cmpl_tokens = response.usage.completion_tokens  # type: ignore
            prompt_tokens = response.usage.prompt_tokens  # type: ignore

            monitor.log_token_usage(key, "openai:" + model, prompt_tokens, cmpl_tokens)

            if len(tools) > 0:
                # Allow retries in case of errors.
                fn_names = [t["name"] for t in tools]
                # Assert that a tool call was made.
                assert (
                    msg.tool_calls is not None and len(msg.tool_calls) > 0
                ), "Tool list provided, but no tool call was made."

                assert (
                    msg.tool_calls[0].function.name in fn_names
                ), f"Unexpected tool name: {msg.tool_calls[0].function.name}"

                try:
                    arguments = json.loads(msg.tool_calls[0].function.arguments)
                except json.JSONDecodeError:
                    print("JSONDecodeError. Function call arguments:")
                    print(msg.tool_calls[0].function.arguments)

                    raise

                return {
                    "name": msg.tool_calls[0].function.name,
                    "arguments": arguments,
                }

            if msg.content is None:
                await aioconsole.aprint("msg.content was None. msg:", msg)

            assert msg.content is not None

            if json_mode or json_schema is not None:
                return json.loads(msg.content)
            else:
                return msg.content
        except Exception as e:
            if "JSON" in str(type(e)).upper():
                await aioconsole.aprint("JSON error:")
                await aioconsole.aprint("Content:", msg.content)
                await aioconsole.aprint(e)

            if i < tries - 1:
                await aioconsole.aprint(f"Error: {e}. Retrying...")
                await asyncio.sleep(backoff)
                backoff = min(30, backoff * 2)
            else:
                await aioconsole.aprint("Reached maximum number of tries. Raising.")
                raise


def create_tool_description(tool: ChatCompletionToolParam):
    name = tool["function"]["name"]
    args_str = ", ".join(
        tool["function"]["parameters"].keys()
        if "parameters" in tool["function"]
        else []
    )

    string = f"Function: {name}({args_str})\n\n"

    if "description" in tool["function"]:
        string += "Description:\n" + tool["function"]["description"] + "\n\n"

    if "parameters" in tool["function"]:
        params: dict = tool["function"]["parameters"]["properties"]  # type: ignore

        string += "Parameters:\n"
        for parameter_name, parameter in params.items():
            string += f"- {parameter_name}"

            if "description" in parameter:
                string += ": " + parameter["description"]

            string += "\n"

        string += "\n\n"

    return string


def _get_openai_client(model_name: str):
    """
    Get from environment variables.
    
    Supports three modes:
    1. LOCAL_MODEL_API_BASE: For locally hosted models (e.g., vllm)
    2. AZURE_OPENAI: For Azure-hosted OpenAI models
    3. Default: Regular OpenAI API
    """

    # Check for locally hosted model first
    # # Support multiple environment variable names for local API base
    # local_api_base = (
    #     os.getenv("LOCAL_MODEL_API_BASE") 
    # )
    # if local_api_base:
    #     # For local models (vllm, etc.), use the base URL with dummy API key
    #     return openai.AsyncOpenAI(
    #         base_url=local_api_base,
    #         api_key="not-needed",  
    #     )
    return openai.AsyncOpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed",  
    )
    
    # Check for Azure OpenAI
    if os.getenv("AZURE_OPENAI", "0") == "1":
        endpoint = os.getenv(f"AZURE_OPENAI_{model_name.replace('-', '_')}_ENDPOINT")
        api_key = os.getenv(f"AZURE_OPENAI_{model_name.replace('-', '_')}_API_KEY")

        assert (
            endpoint is not None and api_key is not None
        ), f"AZURE_OPENAI_*_ENDPOINT and AZURE_OPENAI_*_API_KEY are not set for the model '{model_name}'"

        # Get the API version from the endpoint.
        # Assumes that the endpoint is given in "...?api-version=..." format.
        api_version = endpoint.split("=")[-1]

        return openai.AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
    else:
        # Let OpenAI configure the API key from environment
        return openai.AsyncOpenAI()


class LM:
    def __init__(
        self,
        model: str,
        max_concurrency=10,
        default_kwargs=None,
    ):
        self.model = model
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.client = _get_openai_client(model)
        self.default_kwargs = default_kwargs or {}
        
        # Check if model supports vision/images
        # Most vision models have "vision", "gpt-4o", "gpt-4-turbo", "claude-3" in the name
        # For local models (like Qwen/Qwen3), assume no vision unless explicitly stated
        self.supports_vision = (
            "vision" in model.lower() 
            or "gpt-4o" in model.lower()
            or "gpt-4-turbo" in model.lower()
            or "claude-3" in model.lower()
            or "gemini" in model.lower()
        )

    def is_openai(self) -> bool:
        return isinstance(self.client, (openai.AsyncAzureOpenAI, openai.AsyncOpenAI))

    def is_anthropic(self) -> bool:
        return isinstance(self.client, anthropic.AsyncAnthropic)

    def image_url_content_piece(
        self, image: PIL.Image.Image
    ) -> ChatCompletionContentPartImageParam:
        if self.is_openai():
            return {
                "type": "image_url",
                "image_url": {"url": image_to_data_url(image), "detail": "high"},
            }
        elif self.is_anthropic():
            return {
                "type": "image",  # type: ignore
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_to_base64(image),
                },
            }
        else:
            raise ValueError("Unknown client type.")

    async def __call__(
        self,
        messages: list[ChatCompletionMessageParam],
        json_mode=False,
        json_schema=None,
        tools: list[Function] = [],
        key="general",
        **kwargs,
    ) -> Any:
        async with self.semaphore:
            if self.is_openai():
                client_oai: openai.AsyncOpenAI | openai.AsyncAzureOpenAI = self.client  # type: ignore
                return await completion_openai(
                    client_oai,
                    self.model,
                    messages,
                    json_mode,
                    json_schema,
                    tools,
                    args={**self.default_kwargs, **kwargs},
                    key=key,
                )

    async def json(
        self,
        messages: list[ChatCompletionMessageParam],
        response_model: type[ResponseFormatT],
        **kwargs,
    ) -> ResponseFormatT:
        result = await self.client.beta.chat.completions.parse(
            messages=messages,
            model=self.model,
            response_format=response_model,
        )
        parsed = result.choices[0].message.parsed
        assert parsed is not None
        return parsed
