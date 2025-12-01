"""
Initial skills file for WebArena SkillWeaver evolution

This file contains basic web interaction skills that serve as a starting point
for evolution. OpenEvolve will modify, combine, and create new skills based on
performance on WebArena tasks.
"""


async def click_element_by_selector(page, selector: str, start_path: str = "/", post_click_wait: str = "networkidle"):
    """
    Click an element identified by a flexible selector with safer waits.

    Supports common shorthands like "link=Forums" and "button=Subscribe" in addition to
    plain CSS selectors. Avoids locator.wait_for (which may be unsupported in patched
    environments) by using page.wait_for_selector or role-based locators.

    Args:
        page: The Playwright page object for browser interaction.
        selector: Selector string. Supported:
                  - "link=Forums" (role-based)
                  - "button=Subscribe" (role-based)
                  - CSS like "button:has-text(\"Subscribe\")"
        start_path: Relative path to navigate before attempting the click (default "/").
        post_click_wait: Load state to wait for after click ("load", "domcontentloaded", "networkidle").

    Usage Log:
    - Handled "link=Forums" and "button=Subscribe" reliably on Postmill layouts
    - Clicked CSS "button:has-text('Subscribe')" after page.wait_for_selector
    - Reduced timeouts caused by locator.wait_for unavailability

    Notes:
    - Always uses relative navigation per SkillWeaver requirements
    - Uses .first on locators to avoid strict mode violations when multiple matches exist
    """
    import re

    # Normalize start path to always be relative
    if not start_path.startswith("/"):
        start_path = f"/{start_path}"
    await page.goto(start_path)

    # Role-based shorthand support
    lowered = selector.lower().strip()
    locator = None
    if lowered.startswith("link="):
        name = selector.split("=", 1)[1].strip()
        locator = page.get_by_role("link", name=name).first
    elif lowered.startswith("button="):
        name = selector.split("=", 1)[1].strip()
        locator = page.get_by_role("button", name=name).first

    if locator is None:
        # Fallback to CSS selector with a conservative wait
        try:
            await page.wait_for_selector(selector, state="attached", timeout=5000)
        except Exception:
            # Best-effort: continue to attempt clicking even if wait fails
            pass
        locator = page.locator(selector).first

    await locator.click()
    # Post-click stabilization
    try:
        await page.wait_for_load_state(post_click_wait)
    except Exception:
        # Some clicks do not trigger navigation; ignore
        pass


async def reddit_go_home(page):
    """
    Navigate to the Reddit home feed.

    Args:
        page: The Playwright page object.

    Usage Log:
    - Used as a base before running global searches
    - Helpful reset between workflows
    """
    await page.goto("/")


async def open_subreddit(page, subreddit_name: str):
    """
    Open a subreddit/community by human-readable name (with or without 'r/' prefix).

    On WebArena's Reddit-like (Postmill) layout, communities are served under /f/<name>.
    This function normalizes common inputs and navigates to /f/<name> for better coverage.

    Args:
        page: The Playwright page object.
        subreddit_name: Community name, e.g., "python", "r/python", "/r/python", or "Showerthoughts".

    Usage Log:
    - Opened "DIY" -> /f/DIY successfully on Postmill layout
    - Opened "r/space" and "space" -> /f/space
    - Handles leading slashes and "r/" prefix gracefully
    """
    sub = subreddit_name.strip()
    if sub.startswith("/"):
        sub = sub[1:]
    if sub.lower().startswith("r/"):
        sub = sub[2:]
    await page.goto(f"/f/{sub}")


async def search_reddit(page, query: str, sort: str = None, time_filter: str = None):
    """
    Perform a site-wide search from the home page and optionally apply sort/time filters.

    Args:
        page: The Playwright page object.
        query: Search query text.
        sort: Optional sort order: "Relevance", "Hot", "Top", "New", "Comments".
        time_filter: Optional time filter for "Top": "Hour", "Today", "Week", "Month", "Year", "All".

    Usage Log:
    - Searched "python web scraping" -> results loaded
    - Applied sort="Top" and time_filter="Year" when available
    - Tabs vs menu variations handled by trying multiple roles
    """
    import re

    await page.goto("/")
    await page.get_by_role("textbox", name=re.compile(r"Search", re.I)).fill(query)
    await page.keyboard.press("Enter")

    if sort:
        # Try clicking a tab first, then menu item as fallback
        try:
            await page.get_by_role("tab", name=re.compile(sort, re.I)).click()
        except Exception:
            try:
                await page.get_by_role("button", name=re.compile(r"Sort|Order", re.I)).click()
            except Exception:
                pass
            for role in ("menuitem", "option", "button"):
                try:
                    await page.get_by_role(role, name=re.compile(sort, re.I)).click()
                    break
                except Exception:
                    continue

    if time_filter and sort and sort.lower() == "top":
        # Open time filter control, then choose the desired time range
        try:
            await page.get_by_role("button", name=re.compile(r"(Time|Past|Top)", re.I)).click()
        except Exception:
            pass
        for role in ("menuitem", "option", "button", "link"):
            try:
                await page.get_by_role(role, name=re.compile(time_filter, re.I)).click()
                break
            except Exception:
                continue


async def search_in_subreddit(page, subreddit_name: str, query: str, restrict_to_subreddit: bool = True,
                              sort: str = None, time_filter: str = None):
    """
    Search within a specific subreddit using the community search box.

    Args:
        page: The Playwright page object.
        subreddit_name: Subreddit to search (with or without 'r/' prefix).
        query: Search query string.
        restrict_to_subreddit: If True, attempt to limit results to the subreddit.
        sort: Optional sort: "Relevance", "Hot", "Top", "New", "Comments".
        time_filter: Optional time filter if sort is "Top": "Hour", "Today", "Week", "Month", "Year", "All".

    Usage Log:
    - Searched "weekly thread" in r/python
    - Applied sort="Top" + time="Month" successfully on supported layouts
    - Subreddit scoping toggle varies; attempted when present
    """
    import re

    sub = subreddit_name.strip().lstrip("/")
    if sub.lower().startswith("r/"):
        sub = sub[2:]
    await page.goto(f"/r/{sub}")

    # Use subreddit search input
    await page.get_by_role("textbox", name=re.compile(r"Search", re.I)).fill(query)
    await page.keyboard.press("Enter")

    # Attempt to toggle "in r/<subreddit>" scope if available
    if restrict_to_subreddit:
        try:
            await page.get_by_role("button", name=re.compile(r"(In r/|Show results from)", re.I)).click()
        except Exception:
            pass

    # Optional sorting
    if sort:
        try:
            await page.get_by_role("tab", name=re.compile(sort, re.I)).click()
        except Exception:
            try:
                await page.get_by_role("button", name=re.compile(r"Sort|Order", re.I)).click()
            except Exception:
                pass
            for role in ("menuitem", "option", "button"):
                try:
                    await page.get_by_role(role, name=re.compile(sort, re.I)).click()
                    break
                except Exception:
                    continue

    if time_filter and sort and sort.lower() == "top":
        try:
            await page.get_by_role("button", name=re.compile(r"(Time|Past|Top)", re.I)).click()
        except Exception:
            pass
        for role in ("menuitem", "option", "button", "link"):
            try:
                await page.get_by_role(role, name=re.compile(time_filter, re.I)).click()
                break
            except Exception:
                continue


async def open_post_by_title(page, title_query: str, subreddit_name: str = None, exact: bool = False):
    """
    Open a post by matching its title from home or a specific subreddit.

    Args:
        page: The Playwright page object.
        title_query: Text to match in the post title (substring by default).
        subreddit_name: Optional subreddit scope.
        exact: If True, require exact title match.

    Usage Log:
    - Opened a "Daily Discussion" thread in r/stocks by substring
    - exact=True worked best when full title known
    """
    import re

    start = "/"
    if subreddit_name:
        sub = subreddit_name.strip().lstrip("/")
        if sub.lower().startswith("r/"):
            sub = sub[2:]
        start = f"/r/{sub}"
    await page.goto(start)

    name = title_query if exact else re.compile(re.escape(title_query), re.I)
    article = page.get_by_role("article").filter(has=page.get_by_role("heading", name=name)).first
    await article.get_by_role("link").first.click()


async def open_post_comments_by_title(page, title_query: str, subreddit_name: str = None):
    """
    Open the comments page for a post matched by title.

    Args:
        page: The Playwright page object.
        title_query: Text to match in the post title.
        subreddit_name: Optional subreddit scope.

    Usage Log:
    - Navigated to comments for a post in r/python matching "Weekly"
    """
    import re

    start = "/"
    if subreddit_name:
        sub = subreddit_name.strip().lstrip("/")
        if sub.lower().startswith("r/"):
            sub = sub[2:]
        start = f"/r/{sub}"
    await page.goto(start)

    title_re = re.compile(re.escape(title_query), re.I)
    article = page.get_by_role("article").filter(has=page.get_by_role("heading", name=title_re)).first
    await article.get_by_role("link", name=re.compile(r"comment", re.I)).first.click()


async def sort_home_feed(page, order: str = "Hot"):
    """
    Change the sort order of the home feed.

    Args:
        page: The Playwright page object.
        order: Sort label (e.g., "Hot", "New", "Top", "Rising").

    Usage Log:
    - Switched to "New" before opening the latest post
    """
    import re

    await page.goto("/")
    for role in ("tab", "link", "button"):
        try:
            await page.get_by_role(role, name=re.compile(order, re.I)).click()
            break
        except Exception:
            continue


async def sort_subreddit_feed(page, subreddit_name: str, order: str = "New"):
    """
    Change the sort order of a specific subreddit/community feed.

    On Postmill-style layouts, the control is a button like "Sort by: Hot" that reveals
    a menu or list of links such as "New", "Active", "Top", etc.

    Args:
        page: The Playwright page object.
        subreddit_name: Subreddit/community name (with or without 'r/' prefix).
        order: Sort label (e.g., "Hot", "New", "Active", "Top", "Rising").

    Usage Log:
    - Opened /f/news and set sort to "Top" via the "Sort by:" button
    - Worked on /f/DIY by clicking "Sort by: Hot" then "New"
    """
    import re

    sub = subreddit_name.strip().lstrip("/")
    if sub.lower().startswith("r/"):
        sub = sub[2:]
    await page.goto(f"/f/{sub}")

    # First try direct tab/link/button with the target order
    for role in ("tab", "link", "button"):
        try:
            await page.get_by_role(role, name=re.compile(rf"^{order}$", re.I)).click()
            return
        except Exception:
            continue

    # Fallback: open "Sort by:" control then choose the order
    try:
        await page.get_by_role("button", name=re.compile(r"Sort by:", re.I)).click()
    except Exception:
        # Some pages expose sort options directly as links under the expanded sort menu
        pass

    for role in ("menuitem", "link", "button"):
        try:
            await page.get_by_role(role, name=re.compile(rf"\b{order}\b", re.I)).click()
            return
        except Exception:
            continue


async def open_user_profile(page, username: str):
    """
    Open a user's profile page.

    Args:
        page: The Playwright page object.
        username: Reddit username (with or without 'u/' prefix).

    Usage Log:
    - Opened /user/spez with "spez" and "u/spez"
    """
    user = username.strip()
    if user.startswith("/"):
        user = user[1:]
    if user.lower().startswith("u/"):
        user = user[2:]
    await page.goto(f"/user/{user}")


async def search_posts_by_author(page, author_name: str):
    """
    Search for posts/comments by a specific author using the author: operator.

    Args:
        page: The Playwright page object.
        author_name: Username (with or without 'u/' prefix).

    Usage Log:
    - Found results for u/spez using 'author:spez'
    """
    import re

    author = author_name.strip()
    if author.lower().startswith("u/"):
        author = author[2:]
    await page.goto("/")
    await page.get_by_role("textbox", name=re.compile(r"Search", re.I)).fill(f"author:{author}")
    await page.keyboard.press("Enter")


async def open_forum(page, forum_name: str):
    """
    Open a forum/community page under /f/<forum_name>.

    This is a Postmill-friendly variant useful across WebArena's Reddit instance.

    Args:
        page: The Playwright page object.
        forum_name: Forum/community name as displayed (e.g., "space", "Showerthoughts").

    Usage Log:
    - Navigated to /f/space and /f/Showerthoughts successfully
    """
    name = forum_name.strip().lstrip("/")
    if name.lower().startswith("f/"):
        name = name[2:]
    await page.goto(f"/f/{name}")


async def open_forum_comments_tab(page, forum_name: str):
    """
    Open the Comments tab for a specific forum/community.

    Args:
        page: The Playwright page object.
        forum_name: Forum/community name.

    Usage Log:
    - Opened /f/space then navigated to its Comments tab
    """
    import re
    name = forum_name.strip().lstrip("/")
    if name.lower().startswith("f/"):
        name = name[2:]
    await page.goto(f"/f/{name}")
    await page.get_by_role("link", name=re.compile(r"Comments", re.I)).click()


async def sort_forum_feed(page, forum_name: str, order: str = "New"):
    """
    Sort a forum/community feed using the "Sort by:" control.

    Args:
        page: The Playwright page object.
        forum_name: Forum/community name.
        order: Sort label (e.g., "Hot", "New", "Active", "Top").

    Usage Log:
    - Set "New" on /f/DIY by opening "Sort by:" then clicking "New"
    """
    import re
    name = forum_name.strip().lstrip("/")
    if name.lower().startswith("f/"):
        name = name[2:]
    await page.goto(f"/f/{name}")

    # Try direct link first
    for role in ("tab", "link", "button"):
        try:
            await page.get_by_role(role, name=re.compile(rf"^{order}$", re.I)).click()
            return
        except Exception:
            continue

    # Fallback via "Sort by:" button
    try:
        await page.get_by_role("button", name=re.compile(r"Sort by:", re.I)).click()
    except Exception:
        pass
    for role in ("menuitem", "link", "button"):
        try:
            await page.get_by_role(role, name=re.compile(order, re.I)).click()
            break
        except Exception:
            continue


async def open_forums_index(page):
    """
    Open the Forums index page.

    Args:
        page: The Playwright page object.

    Usage Log:
    - Used before selecting a specific forum; consistent entry point
    """
    await page.goto("/forums")


async def upvote_first_post_on_page(page, start_path: str = "/"):
    """
    Upvote the first visible post article on the given page.

    Args:
        page: The Playwright page object.
        start_path: Relative path to navigate to before upvoting (default "/").

    Usage Log:
    - Upvoted first article on /f/space and on home feed "/"
    - Uses .first to avoid strict mode violations when multiple "Upvote" exist
    """
    import re
    if not start_path.startswith("/"):
        start_path = f"/{start_path}"
    await page.goto(start_path)
    first_article = page.get_by_role("article").filter(has=page.get_by_role("heading")).first
    await first_article.get_by_role("button", name=re.compile(r"Upvote", re.I)).first.click()


async def open_first_post_comments(page, start_path: str = "/"):
    """
    Open the comments link of the first visible post article.

    Args:
        page: The Playwright page object.
        start_path: Relative path to navigate to before opening comments.

    Usage Log:
    - Opened comments from first post on /f/Showerthoughts
    """
    import re
    if not start_path.startswith("/"):
        start_path = f"/{start_path}"
    await page.goto(start_path)
    first_article = page.get_by_role("article").filter(has=page.get_by_role("heading")).first
    await first_article.get_by_role("link", name=re.compile(r"comment", re.I)).first.click()


async def subscribe_to_forum(page, forum_name: str):
    """
    Subscribe to a forum/community using the right sidebar button.

    Args:
        page: The Playwright page object.
        forum_name: Forum/community name.

    Usage Log:
    - Subscribed on /f/space by clicking "Subscribe" in complementary region
    - If already subscribed ("Unsubscribe"), no action taken
    """
    import re
    name = forum_name.strip().lstrip("/")
    if name.lower().startswith("f/"):
        name = name[2:]
    await page.goto(f"/f/{name}")
    # Prefer "Subscribe" if present; ignore if already subscribed
    try:
        await page.get_by_role("button", name=re.compile(r"^Subscribe\b", re.I)).click()
    except Exception:
        # Already subscribed or button hidden; ignore
        pass


async def open_post_in_forum_by_partial_title(page, forum_name: str, title_query: str):
    """
    Open a post within a forum by matching a substring of its title.

    Args:
        page: The Playwright page object.
        forum_name: Forum/community name.
        title_query: Substring to match in the post title.

    Usage Log:
    - Opened first matching post in /f/space using a short fragment of the title
    """
    import re
    name = forum_name.strip().lstrip("/")
    if name.lower().startswith("f/"):
        name = name[2:]
    await page.goto(f"/f/{name}")
    title_re = re.compile(re.escape(title_query), re.I)
    article = page.get_by_role("article").filter(has=page.get_by_role("heading", name=title_re)).first
    await article.get_by_role("link").first.click()


async def open_user_submissions(page, username: str):
    """
    Open the Submissions tab for a given user.

    Args:
        page: The Playwright page object.
        username: Reddit username with or without 'u/' prefix.

    Usage Log:
    - Opened /user/MarvelsGrantMan136/submissions to review posts
    """
    user = username.strip().lstrip("/")
    if user.lower().startswith("u/"):
        user = user[2:]
    await page.goto(f"/user/{user}/submissions")
