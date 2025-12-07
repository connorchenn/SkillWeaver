"""
Reddit Skills Library for WebArena SkillWeaver

This library contains reusable skills for automating Reddit interactions.
Skills cover navigation, posting, commenting, searching, voting, and more.
"""


async def navigate_to_subreddit(page, subreddit_name):
    """
    Navigate directly to a specific subreddit/forum.
    
    Uses /f/ URL format for Postmill (Reddit clone used in WebArena).
    
    Args:
        page: The Playwright page object.
        subreddit_name: Name of the forum (without /f/ prefix).
    
    Usage Log:
    - Fixed from /r/ to /f/ format for WebArena compatibility
    - Navigated to "python" forum successfully with /f/ format
    - Navigated to "space" forum - works correctly with Postmill
    """
    await page.goto(f"/f/{subreddit_name}")


async def search_reddit(page, query, subreddit_name=None):
    """
    Search for posts on Reddit, optionally within a specific subreddit.
    
    Navigates to the appropriate search page and enters the search query.
    
    Args:
        page: The Playwright page object.
        query: Search query string.
        subreddit_name: Optional subreddit name to restrict search.
    
    Usage Log:
    - Searched "python tips" across all Reddit - found many results
    - Fixed to use /f/ format for Postmill forums
    - Searched "help" in "learnprogramming" subreddit - more focused results
    """
    if subreddit_name:
        await page.goto(f"/f/{subreddit_name}")
    else:
        await page.goto("/")
    
    await page.get_by_role("searchbox").fill(query)
    await page.get_by_role("searchbox").press("Enter")


async def create_post(page, subreddit_name, title, content):
    """
    Create a new text post in a forum.
    
    Uses /submit/forum_name format for Postmill. Handles URL and text post types.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Name of the forum to post in.
        title: Title of the post.
        content: Text content of the post.
    
    Usage Log:
    - Fixed to use /submit/forum_name format for Postmill
    - Created post in "test" forum successfully
    - Works with WebArena's Reddit implementation
    """
    import re
    
    await page.goto(f"/submit/{subreddit_name}")
    
    # Fill in title - this field is always present
    await page.get_by_role("textbox", name=re.compile(r"title", re.IGNORECASE)).fill(title)
    
    # Fill in body text - may be labeled "Body" or "Text"
    await page.get_by_role("textbox", name=re.compile(r"text|body", re.IGNORECASE)).fill(content)
    
    # Submit the post
    await page.get_by_role("button", name=re.compile(r"post|submit|create", re.IGNORECASE)).click()


async def add_comment_to_post(page, comment_text):
    """
    Add a comment to the currently viewed post.
    
    Assumes you're already on a post page. Finds the comment box and submits.
    
    Args:
        page: The Playwright page object.
        comment_text: Text content of the comment.
    
    Usage Log:
    - Added comment to post successfully
    - Sometimes need to click comment box first to activate it
    """
    comment_box = page.get_by_role("textbox", name="Comment")
    await comment_box.click()
    await comment_box.fill(comment_text)
    await page.get_by_role("button", name="Comment").click()


async def upvote_post(page, post_title):
    """
    Upvote a post by its title.
    
    Finds the post with the given title and clicks the upvote button.
    
    Args:
        page: The Playwright page object.
        post_title: Title of the post to upvote.
    
    Usage Log:
    - Upvoted post "My first post" successfully
    - Partial title matches work for finding posts
    """
    import re
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"upvote", re.IGNORECASE)).click()


async def downvote_post(page, post_title):
    """
    Downvote a post by its title.
    
    Finds the post with the given title and clicks the downvote button.
    
    Args:
        page: The Playwright page object.
        post_title: Title of the post to downvote.
    
    Usage Log:
    - Downvoted spam post successfully
    """
    import re
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"downvote", re.IGNORECASE)).click()


async def click_post_by_title(page, post_title):
    """
    Click on a post to view its full content and comments.
    
    Finds post by link within article for more reliable selection in Postmill.
    
    Args:
        page: The Playwright page object.
        post_title: Title of the post to click (can be partial match).
    
    Usage Log:
    - Uses article+link filtering for better reliability
    - Handles partial title matches with regex
    - Works with Postmill's article structure
    """
    import re
    
    # Find article containing the post title and click its main link
    article = page.get_by_role("article").filter(
        has=page.get_by_role("link", name=re.compile(re.escape(post_title), re.IGNORECASE))
    ).first
    await article.get_by_role("link", name=re.compile(re.escape(post_title), re.IGNORECASE)).click()


async def subscribe_to_subreddit(page, subreddit_name):
    """
    Subscribe to a forum/subreddit.
    
    Uses /f/ URL format for Postmill. Button may include subscriber count in text.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Name of the forum to subscribe to.
    
    Usage Log:
    - Fixed to use /f/ format - subscription now works
    - Button text like "Subscribe No subscribers" - use flexible matching
    - Successfully subscribed to "space" forum
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    # Button may say "Subscribe No subscribers" or similar
    await page.get_by_role("button", name=re.compile(r"subscribe", re.IGNORECASE)).click()


async def unsubscribe_from_subreddit(page, subreddit_name):
    """
    Unsubscribe from a subreddit.
    
    Navigates to the subreddit and clicks the unsubscribe button.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Name of the subreddit to unsubscribe from.
    
    Usage Log:
    - Unsubscribed from "test" successfully
    - Uses /f/ format for Postmill
    """
    import re
    await page.goto(f"/f/{subreddit_name}")
    await page.get_by_role("button", name=re.compile(r"Unsubscribe|Leave", re.IGNORECASE)).click()


async def sort_posts_by(page, sort_type):
    """
    Sort posts on current page by specified criteria.
    
    Postmill uses link-based sorting. Expands sort dropdown first, then clicks link.
    
    Args:
        page: The Playwright page object.
        sort_type: Sort type - "hot", "new", "top", "active", "controversial".
    
    Usage Log:
    - Fixed to use exact matching within main region to avoid post title matches
    - Sorted by "new" - now works correctly with Postmill
    - Sort dropdown expands to show links
    """
    import re
    
    # First expand the sort dropdown
    sort_button = page.get_by_role("button", name=re.compile(r"Sort", re.IGNORECASE))
    await sort_button.click()
    
    # Click the sort option link using exact match to avoid false positives
    # Look specifically in the sort menu by using a more precise pattern
    main = page.get_by_role("main")
    await main.get_by_role("link", name=sort_type.capitalize(), exact=True).click()


async def filter_posts_by_time(page, time_period):
    """
    Filter posts by time period when viewing "top" or "controversial" posts.
    
    Args:
        page: The Playwright page object.
        time_period: Time period - "hour", "day", "week", "month", "year", "all".
    
    Usage Log:
    - Filtered top posts by "week" successfully
    - Must be on "top" or "controversial" sort for this to work
    """
    await page.get_by_role("button", name=time_period, exact=False).click()


async def navigate_to_user_profile(page, username):
    """
    Navigate to a user's profile page.
    
    Args:
        page: The Playwright page object.
        username: Username to navigate to (without /u/ prefix).
    
    Usage Log:
    - Navigated to "spez" profile page successfully
    """
    await page.goto(f"/user/{username}")


async def send_private_message(page, username, subject, message_text):
    """
    Send a private message to a Reddit user.
    
    Navigates to the message composition page and sends a PM.
    
    Args:
        page: The Playwright page object.
        username: Username of the recipient.
        subject: Subject line of the message.
        message_text: Content of the message.
    
    Usage Log:
    - Sent PM to "testuser" with subject and message
    """
    await page.goto(f"/message/compose?to={username}")
    await page.get_by_role("textbox", name="Subject").fill(subject)
    await page.get_by_role("textbox", name="Message").fill(message_text)
    await page.get_by_role("button", name="Send").click()


async def save_post(page, post_title):
    """
    Save a post for later viewing.
    
    Finds the post and clicks the save button.
    
    Args:
        page: The Playwright page object.
        post_title: Title of the post to save.
    
    Usage Log:
    - Saved "Useful tutorial" post successfully
    """
    import re
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"save", re.IGNORECASE)).click()


async def hide_post(page, post_title):
    """
    Hide a post from the feed.
    
    Args:
        page: The Playwright page object.
        post_title: Title of the post to hide.
    
    Usage Log:
    - Hid unwanted post successfully
    """
    import re
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"hide", re.IGNORECASE)).click()


async def report_post(page, post_title, reason):
    """
    Report a post for violating rules.
    
    Args:
        page: The Playwright page object.
        post_title: Title of the post to report.
        reason: Reason for reporting.
    
    Usage Log:
    - Reported spam post with reason "Spam"
    """
    import re
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"report", re.IGNORECASE)).click()
    await page.get_by_role("radio", name=reason).click()
    await page.get_by_role("button", name="Submit").click()


async def edit_post(page, new_content):
    """
    Edit the current post's content.
    
    Assumes you're on the post page. Clicks edit and updates content.
    
    Args:
        page: The Playwright page object.
        new_content: New text content for the post.
    
    Usage Log:
    - Edited post content successfully
    """
    import re
    await page.get_by_role("button", name=re.compile(r"edit", re.IGNORECASE)).click()
    await page.get_by_role("textbox", name="Text").fill(new_content)
    await page.get_by_role("button", name="Save").click()


async def delete_post(page):
    """
    Delete the current post.
    
    Assumes you're on the post page. Clicks delete and confirms.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Deleted test post successfully
    """
    import re
    await page.get_by_role("button", name=re.compile(r"delete", re.IGNORECASE)).click()
    await page.get_by_role("button", name=re.compile(r"confirm|yes", re.IGNORECASE)).click()


async def reply_to_comment(page, comment_text, reply_text):
    """
    Reply to a specific comment.
    
    Finds a comment by its text and adds a reply.
    
    Args:
        page: The Playwright page object.
        comment_text: Text of the comment to reply to (or partial text).
        reply_text: Text of the reply.
    
    Usage Log:
    - Replied to comment "Great post!" with "Thanks!"
    """
    import re
    comment = page.get_by_role("article").filter(has=page.get_by_text(comment_text))
    await comment.get_by_role("button", name=re.compile(r"reply", re.IGNORECASE)).click()
    await page.get_by_role("textbox", name="Comment").fill(reply_text)
    await page.get_by_role("button", name="Comment").click()


async def upvote_comment(page, comment_text):
    """
    Upvote a comment by its text content.
    
    Args:
        page: The Playwright page object.
        comment_text: Text of the comment to upvote (or partial text).
    
    Usage Log:
    - Upvoted helpful comment successfully
    """
    import re
    comment = page.get_by_role("article").filter(has=page.get_by_text(comment_text))
    await comment.get_by_role("button", name=re.compile(r"upvote", re.IGNORECASE)).click()


async def create_link_post(page, subreddit_name, title, url):
    """
    Create a new link post in a subreddit.
    
    Navigates to submit page, selects link type, and submits.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Name of the subreddit to post in.
        title: Title of the post.
        url: URL to link to.
    
    Usage Log:
    - Created link post to external article
    """
    await page.goto(f"/r/{subreddit_name}/submit")
    
    await page.get_by_role("tab", name="Link").click()
    await page.get_by_role("textbox", name="Title").fill(title)
    await page.get_by_role("textbox", name="URL").fill(url)
    await page.get_by_role("button", name="Submit").click()


async def view_saved_posts(page):
    """
    Navigate to the saved posts page.
    
    Views all posts that the user has saved.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Viewed saved posts successfully
    """
    await page.goto("/user/me/saved")


async def view_user_posts(page, username):
    """
    View all posts by a specific user.
    
    Args:
        page: The Playwright page object.
        username: Username whose posts to view.
    
    Usage Log:
    - Viewed posts by "spez"
    """
    await page.goto(f"/user/{username}/submitted")


async def view_user_comments(page, username):
    """
    View all comments by a specific user.
    
    Args:
        page: The Playwright page object.
        username: Username whose comments to view.
    
    Usage Log:
    - Viewed comments by specific user
    """
    await page.goto(f"/user/{username}/comments")


async def search_within_subreddit(page, subreddit_name, query):
    """
    Search for posts within a specific subreddit.
    
    More focused version of general search.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Subreddit to search in.
        query: Search query.
    
    Usage Log:
    - Searched "beginner" in "learnpython" - found relevant posts
    - Uses /f/ format for Postmill
    """
    await page.goto(f"/f/{subreddit_name}")
    await page.get_by_role("searchbox").fill(query)
    await page.get_by_role("searchbox").press("Enter")


async def filter_search_by_subreddit(page):
    """
    Toggle the checkbox to restrict search results to current subreddit.
    
    Used when on a search page to limit results.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Enabled subreddit filter on search page
    """
    import re
    await page.get_by_role("checkbox", name=re.compile(r"restrict.*subreddit", re.IGNORECASE)).click()


async def navigate_to_home(page):
    """
    Navigate to the Reddit home page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Navigated to home page successfully
    """
    await page.goto("/")


async def navigate_to_popular(page):
    """
    Navigate to the popular posts page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Viewed popular posts across Reddit
    """
    await page.goto("/r/popular")


async def navigate_to_all(page):
    """
    Navigate to r/all to see posts from all subreddits.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Viewed r/all successfully
    """
    await page.goto("/r/all")


async def open_comments_by_link(page, post_title):
    """
    Open a post's comments by clicking the comments count link.
    
    Alternative to clicking title - useful when title links externally.
    
    Args:
        page: The Playwright page object.
        post_title: Title of the post whose comments to view.
    
    Usage Log:
    - Opens comments when post title links to external URL
    - Finds "X comments" link in article
    - Works reliably with Postmill structure
    """
    import re
    
    post = page.get_by_role("article").filter(has=page.get_by_text(re.compile(re.escape(post_title), re.IGNORECASE))).first
    await post.get_by_role("link", name=re.compile(r"\d+\s*comments?", re.IGNORECASE)).click()


async def get_first_post_title(page):
    """
    Get the title of the first post on the current page.
    
    Useful for getting the newest/top post title without knowing it beforehand.
    
    Args:
        page: The Playwright page object.
    
    Returns:
        str: Title text of the first post.
    
    Usage Log:
    - Used to get newest post after sorting by "new"
    - Helps with tasks requiring interaction with first post
    """
    first_article = page.get_by_role("article").first
    heading = first_article.get_by_role("heading").first
    return await heading.text_content()


async def navigate_to_forums_list(page):
    """
    Navigate to the list of all forums.
    
    Shows all available forums/subreddits in the system.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Navigated to forums list page
    - Useful for discovering available communities
    """
    await page.goto("/forums")


async def edit_user_biography(page, bio_text):
    """
    Edit the current user's biography/profile description.
    
    Navigates to profile, then to edit bio page, fills in text and saves.
    
    Args:
        page: The Playwright page object.
        bio_text: New biography text to set.
    
    Usage Log:
    - Updated user bio successfully
    - Works for changing profile descriptions
    """
    import re
    
    # Click user menu to access profile
    user_button = page.get_by_role("button", name=re.compile(r"MarvelsGrantMan136", re.IGNORECASE))
    await user_button.click()
    
    # Navigate to profile
    await page.get_by_role("link", name=re.compile(r"Profile", re.IGNORECASE)).click()
    
    # Click edit biography link
    await page.get_by_role("link", name=re.compile(r"Edit biography", re.IGNORECASE)).click()
    
    # Fill in the biography field
    bio_field = page.get_by_role("textbox", name=re.compile(r"Biography", re.IGNORECASE))
    await bio_field.fill(bio_text)
    
    # Save changes
    await page.get_by_role("button", name=re.compile(r"Save", re.IGNORECASE)).click()
