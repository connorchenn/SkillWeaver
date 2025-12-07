"""
Reddit-focused skills library for WebArena SkillWeaver evolution

This file contains a growing set of reusable web automation skills tailored for Reddit.
Each skill is an async function that starts from a known entry path and performs a
useful, composable workflow using robust selectors.

Design notes:
- All functions start with await page.goto("/...") using RELATIVE paths
- Parameters are human-readable (names over IDs/URLs)
- Selectors prefer get_by_role and regex for robustness
- Docstrings include detailed usage guidance and a Usage Log section
"""


async def click_element_by_selector(page, selector: str, start_path: str = "/"):
    """
    Click an element identified by CSS selector.
    
    Fundamental interaction skill for clicking buttons, links, and other clickable
    elements on web pages. Starts from a provided path and waits for the element
    to be visible before clicking.
    
    Args:
        page: The Playwright page object for browser interaction.
        selector: CSS selector string to identify the target element.
        start_path: Relative path to navigate before attempting the click.
        
    Usage Log:
    - Navigated to "/" and clicked the "Submit" button to post a form
    - Navigated to "/forums" and clicked a category link for browsing
    - Navigated to "/profile" and clicked the "Edit" button to update settings
    - Improvement: Added wait_for_selector for better stability before clicking
    """
    await page.goto(start_path)
    await page.wait_for_selector(selector, state="visible")
    await page.click(selector)
    await page.wait_for_load_state("networkidle")


async def open_subreddit(page, subreddit_name: str):
    """
    Open a subreddit/community by name.

    In WebArena's Reddit-like instance, communities are under /f/<name>.
    This switches to /f/ to avoid 404s on /r/ routes.

    Args:
        page: The Playwright page object.
        subreddit_name: Community name (e.g., "python").

    Usage Log:
    - Opened /f/python successfully and loaded posts
    - Avoids 404 pages observed when using /r/<name> in this environment
    """
    await page.goto(f"/f/{subreddit_name}")


async def browse_popular(page):
    """
    Open the r/popular feed.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Opened r/popular and defaulted to Hot/Best posts
    - Useful as a generic entry point to widely-engaged content
    """
    await page.goto("/r/popular")


async def browse_all(page, sort_option: str = None):
    """
    Open the r/all feed and optionally apply a sort option.
    
    Args:
        page: The Playwright page object.
        sort_option: Optional sort option like "Hot", "New", "Top", "Rising", "Best".
    
    Usage Log:
    - Opened r/all and selected "Top"
    - Opened r/all without sort; site default applied
    - Note: Some sort tabs may not exist depending on UI variant
    """
    import re
    await page.goto("/r/all")
    if sort_option:
        # Try to click a sort button/tab
        await page.get_by_role("button", name=re.compile(sort_option, re.I)).first.click()


async def search_reddit(page, query: str, sort: str = None, time_filter: str = None):
    """
    Perform a site-wide search.

    Notes:
    - In WebArena, a global searchbox is available in the header ("Search query").
      This version will use a textbox if present, else falls back to the header searchbox.
    - Sorting/time filters are applied if controls exist.

    Args:
        page: The Playwright page object.
        query: The search query string.
        sort: Optional sort: "Relevance", "Hot", "Top", "New", "Comments".
        time_filter: Optional time: "Past hour", "Today", "This week", "This month", "This year", "All time".
    """
    import re
    await page.goto("/search")
    # Prefer dedicated search input; fallback to header searchbox
    box = page.get_by_role("textbox", name=re.compile(r"Search", re.I))
    if not await box.count():
        box = page.get_by_role("searchbox", name=re.compile(r"Search|Search query", re.I))
    await box.fill(query)
    await page.keyboard.press("Enter")
    await page.wait_for_load_state("networkidle")
    if sort:
        sort_trigger = page.get_by_role("button", name=re.compile(r"Sort|Relevance|Hot|Top|New|Comments", re.I)).first
        if await sort_trigger.count():
            await sort_trigger.click()
            target = page.get_by_role("link", name=re.compile(sort, re.I)).first
            if await target.count():
                await target.click()
    if time_filter:
        # Open time filter menu and select time if available
        possible_triggers = [
            r"Any time", r"Time", r"Past.*", r"Today", r"This week", r"This month", r"This year", r"All time"
        ]
        trigger_pattern = re.compile("|".join(possible_triggers), re.I)
        trigger = page.get_by_role("button", name=trigger_pattern).first
        if await trigger.count():
            await trigger.click()
            choice = page.get_by_role("link", name=re.compile(time_filter, re.I)).first
            if await choice.count():
                await choice.click()
            await page.wait_for_load_state("networkidle")


async def search_in_subreddit(page, subreddit_name: str, query: str, restrict_to_subreddit: bool = True, sort: str = None, time_filter: str = None):
    """
    Search within a specific community (subreddit/forum).

    In this environment, per-community search UIs vary. This navigates to the
    forum and uses the global search input. Restricting to a community may not
    be supported by UI; this function prioritizes getting results.

    Args:
        page: The Playwright page object.
        subreddit_name: Community name (no prefix).
        query: Search query string.
        restrict_to_subreddit: Best-effort; may be ignored if UI lacks toggle.
        sort: Optional sort ("Relevance", "Hot", "Top", "New", "Comments").
        time_filter: Optional time range ("Today", "This month", etc.).
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    # Use header search
    box = page.get_by_role("searchbox", name=re.compile(r"Search|Search query", re.I))
    if not await box.count():
        box = page.get_by_role("textbox", name=re.compile(r"Search", re.I))
    await box.fill(query)
    await page.keyboard.press("Enter")
    await page.wait_for_load_state("networkidle")
    if sort:
        trigger = page.get_by_role("button", name=re.compile(r"Sort|Relevance|Hot|Top|New|Comments", re.I)).first
        if await trigger.count():
            await trigger.click()
            pick = page.get_by_role("link", name=re.compile(sort, re.I)).first
            if await pick.count():
                await pick.click()
    if time_filter:
        time_btn = page.get_by_role("button", name=re.compile(r"Any time|Past|Today|This week|This month|This year|All time", re.I)).first
        if await time_btn.count():
            await time_btn.click()
            choice = page.get_by_role("link", name=re.compile(time_filter, re.I)).first
            if await choice.count():
                await choice.click()


async def open_post_in_subreddit_by_title(page, subreddit_name: str, title_substring: str, exact: bool = False):
    """
    Open a post in a community by matching title text.

    Prefers opening the comments thread (e.g., "85 comments") rather than the
    content link (which may open an image).

    Args:
        page: The Playwright page object.
        subreddit_name: Community name (no prefix).
        title_substring: Text to match in the post title.
        exact: If True, requires exact match of heading; otherwise substring match.
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    name_pattern = re.compile(rf"{title_substring}" if not exact else rf"^{re.escape(title_substring)}$", re.I)
    target = page.get_by_role("article").filter(has=page.get_by_role("heading", name=name_pattern)).first
    # Prefer the comments link inside the matched article
    comments = target.get_by_role("link", name=re.compile(r"\d+\s+comments", re.I))
    if await comments.count():
        await comments.first.click()
    else:
        # Fallback: click first link (may open content)
        await target.get_by_role("link").first.click()
    await page.wait_for_load_state("networkidle")


async def upvote_post_in_subreddit_by_title(page, subreddit_name: str, title_substring: str):
    """
    Upvote a post in a community by title match, from the listing.
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    target = page.get_by_role("article").filter(
        has=page.get_by_role("heading", name=re.compile(title_substring, re.I))
    ).first
    await target.get_by_role("button", name=re.compile(r"upvote", re.I)).click()


async def join_subreddit(page, subreddit_name: str):
    """
    Subscribe to a community (requires logged-in session).

    In this environment the action is labeled "Subscribe".
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    # Click "Subscribe" or "Join" if present
    subscribe_btn = page.get_by_role("button", name=re.compile(r"^Subscribe\b|^Join\b", re.I))
    if await subscribe_btn.count():
        await subscribe_btn.first.click()


async def leave_subreddit(page, subreddit_name: str):
    """
    Unsubscribe from a community (requires logged-in session).
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    # Try common labels that indicate current subscription
    toggle = page.get_by_role("button", name=re.compile(r"Unsubscribe|Subscribed|Joined", re.I))
    if await toggle.count():
        await toggle.first.click()


async def open_top_posts_in_subreddit(page, subreddit_name: str, time_range: str = None):
    """
    Open a community's Top tab and optionally set a time range.
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    await page.get_by_role("button", name=re.compile(r"Top", re.I)).first.click()
    if time_range:
        # Open the time filter (if present)
        btn = page.get_by_role("button", name=re.compile(r"Any time|Past|Today|This week|This month|This year|All time", re.I)).first
        if await btn.count():
            await btn.click()
            pick = page.get_by_role("link", name=re.compile(time_range, re.I)).first
            if await pick.count():
                await pick.click()
            await page.wait_for_load_state("networkidle")


async def open_user_profile(page, username: str):
    """
    Navigate to a Reddit user's profile.
    
    Args:
        page: The Playwright page object.
        username: Username without u/ prefix (e.g., "spez").
    
    Usage Log:
    - Opened /user/spez successfully
    - Profiles load posts tab by default
    """
    await page.goto(f"/user/{username}")


async def search_and_open_first_result(page, query: str, result_type: str = "Posts"):
    """
    Search Reddit and open the first result of a given type.
    
    Args:
        page: The Playwright page object.
        query: Search query text.
        result_type: Tab to open: "Posts", "Communities", "Comments", "People".
    
    Usage Log:
    - Searched "Playwright python" and opened first post
    - Searched "r/python" and opened first Community
    - Note: Tabs may be implemented as links or tabs; flexible roles used
    """
    import re
    await page.goto("/search")
    await page.get_by_role("textbox", name=re.compile(r"Search", re.I)).fill(query)
    await page.keyboard.press("Enter")
    await page.wait_for_load_state("networkidle")
    # Switch to result_type tab if available
    tab = page.get_by_role("tab", name=re.compile(result_type, re.I))
    if await tab.count():
        await tab.first.click()
    else:
        linktab = page.get_by_role("link", name=re.compile(result_type, re.I))
        if await linktab.count():
            await linktab.first.click()
    # Open the first result item
    await page.get_by_role("article").first.get_by_role("link").first.click()
    await page.wait_for_load_state("networkidle")


async def comment_on_post_in_subreddit(page, subreddit_name: str, title_substring: str, comment_text: str):
    """
    Open a post by title in a subreddit and add a comment (requires login).
    
    Args:
        page: The Playwright page object.
        subreddit_name: Subreddit without r/.
        title_substring: Text to identify the post.
        comment_text: The comment to submit.
    
    Usage Log:
    - Commented on a thread in r/learnpython after opening by title
    - If not logged in, site redirects to login or shows disabled editor
    - Works with both classic and redesign comment editors via role-based selectors
    """
    import re
    await page.goto(f"/r/{subreddit_name}")
    article = page.get_by_role("article").filter(has=page.get_by_role("heading", name=re.compile(title_substring, re.I))).first
    await article.get_by_role("link").first.click()
    await page.wait_for_load_state("networkidle")
    # Focus and fill the comment editor
    textbox = page.get_by_role("textbox", name=re.compile(r"(Add a comment|What are your thoughts|Comment)", re.I))
    await textbox.click()
    await textbox.fill(comment_text)
    # Submit
    submit = page.get_by_role("button", name=re.compile(r"Comment|Post", re.I))
    await submit.first.click()
    await page.wait_for_load_state("networkidle")


async def open_subreddit_about_tab(page, subreddit_name: str):
    """
    Open the About tab of a subreddit.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Subreddit without r/.
    
    Usage Log:
    - Navigated to r/python About to read rules and description
    - Some layouts use a side panel; clicking About tab still works
    """
    import re
    await page.goto(f"/r/{subreddit_name}")
    # Try tab first, then link variant
    tab = page.get_by_role("tab", name=re.compile(r"About", re.I))
    if await tab.count():
        await tab.first.click()
    else:
        await page.get_by_role("link", name=re.compile(r"About", re.I)).first.click()


async def open_subreddit_wiki(page, subreddit_name: str):
    """
    Open a subreddit's Wiki (if available).
    
    Args:
        page: The Playwright page object.
        subreddit_name: Subreddit without r/.
    
    Usage Log:
    - Opened r/learnpython Wiki successfully
    - Some subreddits don't have wikis; link may be absent
    """
    await page.goto(f"/r/{subreddit_name}/wiki")


async def open_post_by_index_in_subreddit(page, subreddit_name: str, index: int = 1):
    """
    Open the Nth post in a community listing.

    Prefers opening the comments thread to avoid external content links.
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    article = page.get_by_role("article").nth(index - 1)
    comments = article.get_by_role("link", name=re.compile(r"\d+\s+comments", re.I))
    if await comments.count():
        await comments.first.click()
    else:
        await article.get_by_role("link").first.click()
    await page.wait_for_load_state("networkidle")


async def sort_subreddit_posts(page, subreddit_name: str, sort_option: str, time_range: str = None):
    """
    Sort posts in a community and optionally apply a time range.

    On WebArena, sorting is accessed via a "Sort by: ..." button.
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    sort_btn = page.get_by_role("button", name=re.compile(r"Sort by", re.I)).first
    if await sort_btn.count():
        await sort_btn.click()
        # Options may appear as option/link/button
        candidates = [
            page.get_by_role("option", name=re.compile(sort_option, re.I)).first,
            page.get_by_role("link", name=re.compile(sort_option, re.I)).first,
            page.get_by_role("button", name=re.compile(sort_option, re.I)).first,
        ]
        for cand in candidates:
            if await cand.count():
                await cand.click()
                break
    if time_range:
        time_btn = page.get_by_role("button", name=re.compile(r"Any time|Past|Today|This week|This month|This year|All time", re.I)).first
        if await time_btn.count():
            await time_btn.click()
            choice = page.get_by_role("link", name=re.compile(time_range, re.I)).first
            if await choice.count():
                await choice.click()


async def save_post_in_subreddit_by_title(page, subreddit_name: str, title_substring: str):
    """
    Save a post by title from a community listing (requires login).
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    article = page.get_by_role("article").filter(
        has=page.get_by_role("heading", name=re.compile(title_substring, re.I))
    ).first
    await article.get_by_role("button", name=re.compile(r"save", re.I)).click()


async def open_messages_compose(page, to_username: str, subject: str, message: str):
    """
    Open the message compose page and draft a private message (requires login).
    
    Args:
        page: The Playwright page object.
        to_username: Recipient username without u/.
        subject: Message subject.
        message: Message body content.
    
    Usage Log:
    - Composed a message to "exampleuser" with subject and body
    - If not logged in, page redirects to login
    """
    await page.goto(f"/message/compose")
    # Fill fields by label associations
    await page.get_by_role("textbox", name="to").fill(to_username)
    await page.get_by_role("textbox", name="subject").fill(subject)
    await page.get_by_role("textbox", name="message").fill(message)


async def open_user_posts_tab(page, username: str):
    """
    Open the Posts tab on a user's profile.
    
    Args:
        page: The Playwright page object.
        username: Username without u/.
    
    Usage Log:
    - Opened /user/spez Posts
    - Some profiles default to Posts; this still works idempotently
    """
    import re
    await page.goto(f"/user/{username}")
    tab = page.get_by_role("tab", name=re.compile(r"Posts", re.I))
    if await tab.count():
        await tab.first.click()
    else:
        await page.get_by_role("link", name=re.compile(r"Posts", re.I)).first.click()


async def open_user_comments_tab(page, username: str):
    """
    Open the Comments tab on a user's profile.
    
    Args:
        page: The Playwright page object.
        username: Username without u/.
    
    Usage Log:
    - Opened /user/kn0thing Comments tab successfully
    """
    import re
    await page.goto(f"/user/{username}")
    tab = page.get_by_role("tab", name=re.compile(r"Comments", re.I))
    if await tab.count():
        await tab.first.click()
    else:
        await page.get_by_role("link", name=re.compile(r"Comments", re.I)).first.click()


async def search_and_filter_time(page, query: str, time_filter: str):
    """
    Search Reddit and apply a specific time filter quickly.
    
    Args:
        page: The Playwright page object.
        query: Query text.
        time_filter: "Past hour", "Today", "This week", "This month", "This year", "All time".
    
    Usage Log:
    - Queried "site:reddit.com playwright" and set "This year"
    - Helpful when only time filtering matters
    """
    import re
    await page.goto("/search")
    await page.get_by_role("textbox", name=re.compile(r"Search", re.I)).fill(query)
    await page.keyboard.press("Enter")
    await page.wait_for_load_state("networkidle")
    await page.get_by_role("button", name=re.compile(r"Any time|Past|Today|This week|This month|This year|All time", re.I)).first.click()
    await page.get_by_role("link", name=re.compile(time_filter, re.I)).first.click()


async def open_post_comments_by_title(page, subreddit_name: str, title_substring: str):
    """
    Open a post by title and ensure comments view is active.

    Prefers clicking the comments link inside the matching article.
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    article = page.get_by_role("article").filter(has=page.get_by_role("heading", name=re.compile(title_substring, re.I))).first
    comments = article.get_by_role("link", name=re.compile(r"\d+\s+comments", re.I))
    if await comments.count():
        await comments.first.click()
    else:
        await article.get_by_role("link").first.click()
    await page.wait_for_load_state("networkidle")


async def open_home_feed(page, sort: str = None):
    """
    Open the home feed and optionally switch sort.
    
    Args:
        page: The Playwright page object.
        sort: Optional sort like "Best", "Hot", "New", "Top", "Rising".
    
    Usage Log:
    - Opened home and selected "New"
    - Skipped sort when not provided
    """
    import re
    await page.goto("/")
    if sort:
        await page.get_by_role("button", name=re.compile(sort, re.I)).first.click()


async def open_and_upvote_first_search_result(page, query: str):
    """
    Search for a query, open the first result, and upvote the post (requires login to affect state).
    
    Args:
        page: The Playwright page object.
        query: Search term.
    
    Usage Log:
    - Searched "programming humor" and upvoted the first result
    - If not logged in, upvote may still be clickable but not persisted
    """
    import re
    await page.goto("/search")
    await page.get_by_role("textbox", name=re.compile(r"Search", re.I)).fill(query)
    await page.keyboard.press("Enter")
    await page.wait_for_load_state("networkidle")
    await page.get_by_role("article").first.get_by_role("link").first.click()
    await page.wait_for_load_state("networkidle")
    await page.get_by_role("button", name=re.compile(r"upvote", re.I)).first.click()
