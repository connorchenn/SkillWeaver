"""
Comprehensive Reddit Skills Library for WebArena SkillWeaver

This library contains reusable skills for automating Reddit interactions.
Skills cover posting, commenting, searching, voting, user interactions,
subreddit navigation, and more.
"""


# ============================================================================
# NAVIGATION SKILLS
# ============================================================================

async def go_to_homepage(page):
    """
    Navigate to Reddit homepage.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Basic navigation starting point for many workflows
    """
    await page.goto("/")


async def go_to_subreddit(page, subreddit_name):
    """
    Navigate to a specific forum (subreddit equivalent in Postmill).
    
    Args:
        page: The Playwright page object.
        subreddit_name: Name of the forum (without f/ prefix).
    
    Usage Log:
    - Navigate to specific communities for browsing or posting
    - Postmill uses /f/ prefix for forums, not /r/
    """
    await page.goto(f"/f/{subreddit_name}")


async def go_to_user_profile(page, username):
    """
    Navigate to a user's profile page.
    
    Args:
        page: The Playwright page object.
        username: Username (without u/ prefix).
    
    Usage Log:
    - View user posts, comments, and profile information
    """
    await page.goto(f"/user/{username}")


async def go_to_submit_page(page):
    """
    Navigate to the submit/create post page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Starting point for creating new posts
    """
    await page.goto("/submit")


async def go_to_forums_list(page):
    """
    Navigate to the forums list page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Browse available forums/communities
    - Starting point for discovering new forums
    """
    await page.goto("/forums")


async def go_to_search(page):
    """
    Navigate to search page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Entry point for searching posts and content
    """
    await page.goto("/search")


# ============================================================================
# POST CREATION SKILLS
# ============================================================================

async def create_text_post(page, subreddit_name, title, text_content):
    """
    Create a new text post in a subreddit.
    
    Navigates to submit page, selects subreddit, fills title and text,
    then submits the post.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Target subreddit name.
        title: Post title.
        text_content: Post body text.
    
    Usage Log:
    - Created discussion posts successfully
    - Title and text fields accept markdown formatting
    """
    import re
    
    await page.goto("/submit")
    
    # Select subreddit
    await page.get_by_role("combobox", name=re.compile(r"choose a community", re.IGNORECASE)).fill(subreddit_name)
    await page.get_by_role("option", name=subreddit_name).click()
    
    # Fill title
    await page.get_by_role("textbox", name=re.compile(r"title", re.IGNORECASE)).fill(title)
    
    # Fill text content
    await page.get_by_role("textbox", name=re.compile(r"text|body", re.IGNORECASE)).fill(text_content)
    
    # Submit
    await page.get_by_role("button", name=re.compile(r"post|submit", re.IGNORECASE)).click()


async def create_link_post(page, subreddit_name, title, url):
    """
    Create a new link post in a subreddit.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Target subreddit name.
        title: Post title.
        url: URL to link to.
    
    Usage Log:
    - Share external links and articles
    """
    import re
    
    await page.goto("/submit")
    
    # Select link/URL tab
    await page.get_by_role("tab", name=re.compile(r"link|url", re.IGNORECASE)).click()
    
    # Select subreddit
    await page.get_by_role("combobox", name=re.compile(r"choose a community", re.IGNORECASE)).fill(subreddit_name)
    await page.get_by_role("option", name=subreddit_name).click()
    
    # Fill title
    await page.get_by_role("textbox", name=re.compile(r"title", re.IGNORECASE)).fill(title)
    
    # Fill URL
    await page.get_by_role("textbox", name=re.compile(r"url|link", re.IGNORECASE)).fill(url)
    
    # Submit
    await page.get_by_role("button", name=re.compile(r"post|submit", re.IGNORECASE)).click()


# ============================================================================
# COMMENT SKILLS
# ============================================================================

async def add_comment_to_post(page, post_title, comment_text):
    """
    Add a comment to a post identified by title.
    
    Searches for the post, opens it, and adds a comment.
    
    Args:
        page: The Playwright page object.
        post_title: Title of the post to comment on.
        comment_text: Comment content.
    
    Usage Log:
    - Successfully added comments to discussions
    - Works when post is visible on current page
    """
    import re
    
    # Find and click the post
    await page.get_by_role("link", name=post_title).click()
    
    # Find comment box and add comment
    await page.get_by_role("textbox", name=re.compile(r"comment", re.IGNORECASE)).fill(comment_text)
    await page.get_by_role("button", name=re.compile(r"comment|save", re.IGNORECASE)).click()


async def reply_to_comment(page, parent_comment_text, reply_text):
    """
    Reply to a specific comment.
    
    Finds a comment by its text content and adds a reply.
    
    Args:
        page: The Playwright page object.
        parent_comment_text: Text content of the comment to reply to.
        reply_text: Reply content.
    
    Usage Log:
    - Engage in comment threads
    - Partial text matching helps find comments
    """
    import re
    
    # Find the comment and click reply
    comment = page.get_by_text(parent_comment_text)
    await comment.get_by_role("button", name=re.compile(r"reply", re.IGNORECASE)).click()
    
    # Fill and submit reply
    await page.get_by_role("textbox", name=re.compile(r"comment", re.IGNORECASE)).fill(reply_text)
    await page.get_by_role("button", name=re.compile(r"comment|save", re.IGNORECASE)).click()


# ============================================================================
# VOTING SKILLS
# ============================================================================

async def upvote_post(page, post_title):
    """
    Upvote a post by title.
    
    Args:
        page: The Playwright page object.
        post_title: Title of post to upvote.
    
    Usage Log:
    - Quick upvoting from feed or subreddit view
    """
    import re
    
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"upvote", re.IGNORECASE)).click()


async def downvote_post(page, post_title):
    """
    Downvote a post by title.
    
    Args:
        page: The Playwright page object.
        post_title: Title of post to downvote.
    
    Usage Log:
    - Express disagreement or mark low-quality content
    """
    import re
    
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"downvote", re.IGNORECASE)).click()


async def upvote_comment(page, comment_text):
    """
    Upvote a comment by its text content.
    
    Args:
        page: The Playwright page object.
        comment_text: Text content of comment to upvote.
    
    Usage Log:
    - Support helpful or insightful comments
    """
    import re
    
    comment = page.get_by_text(comment_text)
    await comment.get_by_role("button", name=re.compile(r"upvote", re.IGNORECASE)).click()


# ============================================================================
# SEARCH SKILLS
# ============================================================================

async def search_posts(page, query):
    """
    Search for posts using a query string.
    
    Args:
        page: The Playwright page object.
        query: Search query text.
    
    Usage Log:
    - Basic post searching across all forums
    - Uses searchbox in header for quick searches
    """
    import re
    
    # Use the search box in the header
    await page.get_by_role("searchbox", name=re.compile(r"search", re.IGNORECASE)).fill(query)
    await page.get_by_role("searchbox", name=re.compile(r"search", re.IGNORECASE)).press("Enter")


async def search_in_subreddit(page, subreddit_name, query):
    """
    Search within a specific forum (subreddit equivalent).
    
    Args:
        page: The Playwright page object.
        subreddit_name: Forum name to search in.
        query: Search query text.
    
    Usage Log:
    - Find posts within specific communities
    - Updated for Postmill's /f/ URL pattern
    """
    import re
    
    await page.goto(f"/f/{subreddit_name}")
    await page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE)).fill(query)
    await page.get_by_role("button", name=re.compile(r"search", re.IGNORECASE)).click()


async def search_posts_by_author(page, username):
    """
    Search for posts by a specific author.
    
    Args:
        page: The Playwright page object.
        username: Username to search for.
    
    Usage Log:
    - Find all posts from a specific user
    """
    await page.goto("/search")
    await page.get_by_role("textbox", name="search").fill(f"author:{username}")
    await page.get_by_role("button", name="search").click()


async def search_posts_by_flair(page, flair_text):
    """
    Search for posts with specific flair.
    
    Args:
        page: The Playwright page object.
        flair_text: Flair text to search for.
    
    Usage Log:
    - Find posts tagged with specific categories
    """
    import re
    
    await page.goto("/search")
    await page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE)).fill(f"flair:{flair_text}")
    await page.get_by_role("button", name=re.compile(r"search", re.IGNORECASE)).click()


async def search_posts_by_url(page, url):
    """
    Search for posts linking to a specific URL.
    
    Args:
        page: The Playwright page object.
        url: URL to search for.
    
    Usage Log:
    - Find discussions about specific links
    """
    import re
    
    await page.goto("/search")
    await page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE)).fill(f"url:{url}")
    await page.get_by_role("button", name=re.compile(r"search", re.IGNORECASE)).click()


async def search_posts_in_timeframe(page, query, timeframe):
    """
    Search posts within a specific timeframe.
    
    Args:
        page: The Playwright page object.
        query: Search query.
        timeframe: Time period (e.g., "hour", "day", "week", "month", "year").
    
    Usage Log:
    - Find recent or historical posts
    """
    import re
    
    await page.goto("/search")
    await page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE)).fill(query)
    await page.get_by_role("button", name=re.compile(r"search", re.IGNORECASE)).click()
    
    # Apply time filter
    await page.get_by_role("button", name=re.compile(r"time|filter", re.IGNORECASE)).click()
    await page.get_by_role("menuitem", name=re.compile(timeframe, re.IGNORECASE)).click()


# ============================================================================
# POST INTERACTION SKILLS
# ============================================================================

async def save_post(page, post_title):
    """
    Save a post for later viewing.
    
    Args:
        page: The Playwright page object.
        post_title: Title of post to save.
    
    Usage Log:
    - Bookmark interesting posts
    """
    import re
    
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"save", re.IGNORECASE)).click()


async def hide_post(page, post_title):
    """
    Hide a post from view.
    
    Args:
        page: The Playwright page object.
        post_title: Title of post to hide.
    
    Usage Log:
    - Remove unwanted content from feed
    """
    import re
    
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"hide", re.IGNORECASE)).click()


async def share_post(page, post_title):
    """
    Open share dialog for a post.
    
    Args:
        page: The Playwright page object.
        post_title: Title of post to share.
    
    Usage Log:
    - Get shareable link or share to other platforms
    """
    import re
    
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"share", re.IGNORECASE)).click()


async def report_post(page, post_title, reason):
    """
    Report a post for rule violations.
    
    Args:
        page: The Playwright page object.
        post_title: Title of post to report.
        reason: Report reason.
    
    Usage Log:
    - Flag inappropriate content
    """
    import re
    
    post = page.get_by_role("article").filter(has=page.get_by_text(post_title))
    await post.get_by_role("button", name=re.compile(r"report", re.IGNORECASE)).click()
    
    # Select reason
    await page.get_by_role("radio", name=reason).click()
    await page.get_by_role("button", name=re.compile(r"submit|report", re.IGNORECASE)).click()


# ============================================================================
# SUBREDDIT INTERACTION SKILLS
# ============================================================================

async def join_subreddit(page, subreddit_name):
    """
    Subscribe to a forum (subreddit equivalent).
    
    Args:
        page: The Playwright page object.
        subreddit_name: Forum name to join.
    
    Usage Log:
    - Add forum to personal feed
    - Uses /f/ URL pattern for Postmill forums
    """
    import re
    
    await page.goto(f"/f/{subreddit_name}")
    await page.get_by_role("button", name=re.compile(r"join|subscribe", re.IGNORECASE)).click()


async def leave_subreddit(page, subreddit_name):
    """
    Unsubscribe from a forum (subreddit equivalent).
    
    Args:
        page: The Playwright page object.
        subreddit_name: Forum name to leave.
    
    Usage Log:
    - Remove forum from personal feed
    - Uses /f/ URL pattern for Postmill forums
    """
    import re
    
    await page.goto(f"/f/{subreddit_name}")
    await page.get_by_role("button", name=re.compile(r"leave|unsubscribe|joined", re.IGNORECASE)).click()


# ============================================================================
# FILTERING AND SORTING SKILLS
# ============================================================================

async def sort_posts_by_hot(page):
    """
    Sort posts by hot (trending).
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - See currently trending content
    """
    import re
    
    await page.get_by_role("button", name=re.compile(r"sort", re.IGNORECASE)).click()
    await page.get_by_role("menuitem", name=re.compile(r"hot", re.IGNORECASE)).click()


async def sort_posts_by_new(page):
    """
    Sort posts by newest first.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - See most recent posts
    - Essential for finding latest content in forums
    """
    import re
    
    # Check if already on New sort by looking at current button text
    sort_button = page.get_by_role("button", name=re.compile(r"sort", re.IGNORECASE))
    button_text = await sort_button.text_content()
    
    if "new" not in button_text.lower():
        await sort_button.click()
        await page.get_by_role("menuitem", name=re.compile(r"new", re.IGNORECASE)).click()


async def sort_posts_by_top(page):
    """
    Sort posts by top rated.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - See highest voted content
    """
    import re
    
    await page.get_by_role("button", name=re.compile(r"sort", re.IGNORECASE)).click()
    await page.get_by_role("menuitem", name=re.compile(r"top", re.IGNORECASE)).click()


async def filter_top_posts_by_timeframe(page, timeframe):
    """
    Filter top posts by time period.
    
    Args:
        page: The Playwright page object.
        timeframe: Time period (e.g., "Today", "This Week", "This Month", "All Time").
    
    Usage Log:
    - View top content from specific time periods
    """
    import re
    
    await page.get_by_role("combobox", name=re.compile(r"time", re.IGNORECASE)).select_option(timeframe)


# ============================================================================
# USER INTERACTION SKILLS
# ============================================================================

async def send_private_message(page, username, subject, message):
    """
    Send a private message to a user.
    
    Args:
        page: The Playwright page object.
        username: Recipient username.
        subject: Message subject.
        message: Message body.
    
    Usage Log:
    - Direct communication with other users
    """
    import re
    
    await page.goto(f"/message/compose/?to={username}")
    await page.get_by_role("textbox", name=re.compile(r"subject", re.IGNORECASE)).fill(subject)
    await page.get_by_role("textbox", name=re.compile(r"message", re.IGNORECASE)).fill(message)
    await page.get_by_role("button", name=re.compile(r"send", re.IGNORECASE)).click()


async def follow_user(page, username):
    """
    Follow a user to see their posts.
    
    Args:
        page: The Playwright page object.
        username: Username to follow.
    
    Usage Log:
    - Stay updated on specific user's content
    """
    import re
    
    await page.goto(f"/user/{username}")
    await page.get_by_role("button", name=re.compile(r"follow", re.IGNORECASE)).click()


async def edit_user_biography(page, biography_text):
    """
    Edit the current user's biography.
    
    Navigates through user settings to edit biography.
    
    Args:
        page: The Playwright page object.
        biography_text: New biography text to set.
    
    Usage Log:
    - Update user profile information
    - Accessed through user dropdown menu
    """
    import re
    
    # Click on user profile button (expanded state shows it's a dropdown)
    await page.get_by_role("button", name=re.compile(r"MarvelsGrantMan136", re.IGNORECASE)).click()
    
    # Navigate to user settings or profile edit
    await page.get_by_role("link", name=re.compile(r"user settings|preferences", re.IGNORECASE)).click()
    
    # Find and click edit biography link
    await page.get_by_role("link", name=re.compile(r"edit biography", re.IGNORECASE)).click()
    
    # Fill biography textbox
    await page.get_by_role("textbox", name=re.compile(r"biography", re.IGNORECASE)).fill(biography_text)
    
    # Save changes
    await page.get_by_role("button", name=re.compile(r"save", re.IGNORECASE)).click()


async def block_user(page, username):
    """
    Block a user.
    
    Args:
        page: The Playwright page object.
        username: Username to block.
    
    Usage Log:
    - Prevent interactions with specific users
    """
    import re
    
    await page.goto(f"/user/{username}")
    await page.get_by_role("button", name=re.compile(r"more|options", re.IGNORECASE)).click()
    await page.get_by_role("menuitem", name=re.compile(r"block", re.IGNORECASE)).click()
    await page.get_by_role("button", name=re.compile(r"confirm|block", re.IGNORECASE)).click()


# ============================================================================
# COMPOSITE WORKFLOW SKILLS
# ============================================================================

async def find_and_upvote_post(page, search_query):
    """
    Search for a post and upvote the first result.
    
    Composite skill combining search and voting.
    
    Args:
        page: The Playwright page object.
        search_query: Search query to find the post.
    
    Usage Log:
    - Quick workflow for supporting content
    """
    import re
    
    await page.goto("/search")
    await page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE)).fill(search_query)
    await page.get_by_role("button", name=re.compile(r"search", re.IGNORECASE)).click()
    
    # Upvote first result
    first_post = page.get_by_role("article").first
    await first_post.get_by_role("button", name=re.compile(r"upvote", re.IGNORECASE)).click()


async def create_post_and_comment(page, subreddit_name, title, text_content, comment_text):
    """
    Create a post and immediately add a comment to it.
    
    Composite skill for posting with additional context.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Target subreddit.
        title: Post title.
        text_content: Post body.
        comment_text: First comment to add.
    
    Usage Log:
    - Add clarifying information or sources immediately after posting
    """
    import re
    
    await page.goto("/submit")
    
    # Create post
    await page.get_by_role("combobox", name=re.compile(r"choose a community", re.IGNORECASE)).fill(subreddit_name)
    await page.get_by_role("option", name=subreddit_name).click()
    await page.get_by_role("textbox", name=re.compile(r"title", re.IGNORECASE)).fill(title)
    await page.get_by_role("textbox", name=re.compile(r"text|body", re.IGNORECASE)).fill(text_content)
    await page.get_by_role("button", name=re.compile(r"post|submit", re.IGNORECASE)).click()
    
    # Add comment
    await page.get_by_role("textbox", name=re.compile(r"comment", re.IGNORECASE)).fill(comment_text)
    await page.get_by_role("button", name=re.compile(r"comment|save", re.IGNORECASE)).click()


async def navigate_to_forum_from_list(page, forum_name):
    """
    Navigate to forums list and click on a specific forum.
    
    Args:
        page: The Playwright page object.
        forum_name: Name of forum to navigate to.
    
    Usage Log:
    - Browse forums list and select specific community
    - Useful when exact forum URL is unknown
    - Handles Postmill forum name format (e.g., "Showerthoughts — Showerthoughts")
    """
    import re
    
    await page.goto("/forums")
    
    # Try exact forum name first
    try:
        await page.get_by_role("link", name=re.compile(forum_name, re.IGNORECASE)).click()
    except:
        # If not found, try navigating directly via URL
        await page.goto(f"/f/{forum_name}")


async def go_to_showerthoughts(page):
    """
    Navigate directly to Showerthoughts forum.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Quick navigation to popular Showerthoughts forum
    - Commonly used in test scenarios
    """
    await page.goto("/f/Showerthoughts")


async def search_forums_list(page, query):
    """
    Search for forums by name in the forums directory.
    
    Args:
        page: The Playwright page object.
        query: Forum name or keyword to search for.
    
    Usage Log:
    - Find forums when browsing directory
    - Alternative to direct URL navigation
    """
    await page.goto("/forums")
    
    # Use page search if available
    await page.get_by_role("searchbox", name=re.compile(r"search", re.IGNORECASE)).fill(query)
    await page.keyboard.press("Enter")


async def filter_posts_by_featured(page):
    """
    Filter posts to show only featured content.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - View curated/featured posts
    - Uses Postmill's filtering system
    """
    import re
    
    await page.get_by_role("button", name=re.compile(r"filter", re.IGNORECASE)).click()
    await page.get_by_role("menuitem", name=re.compile(r"featured", re.IGNORECASE)).click()


async def filter_posts_by_subscribed(page):
    """
    Filter posts to show only from subscribed forums.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - View personalized feed from joined forums
    """
    import re
    
    await page.get_by_role("button", name=re.compile(r"filter", re.IGNORECASE)).click()
    await page.get_by_role("menuitem", name=re.compile(r"subscribed", re.IGNORECASE)).click()


async def search_join_and_post(page, subreddit_name, post_title, post_text):
    """
    Navigate to a forum, join it, and create a post.
    
    Complete workflow for discovering and contributing to new communities.
    
    Args:
        page: The Playwright page object.
        subreddit_name: Forum name to find and join.
        post_title: Title for new post.
        post_text: Content for new post.
    
    Usage Log:
    - Onboarding workflow for new community participation
    - Updated for Postmill's /f/ URL pattern
    """
    import re
    
    # Navigate to forum and join
    await page.goto(f"/f/{subreddit_name}")
    await page.get_by_role("button", name=re.compile(r"join|subscribe", re.IGNORECASE)).click()
    
    # Create post
    await page.goto("/submit")
    await page.get_by_role("combobox", name=re.compile(r"choose a community", re.IGNORECASE)).fill(subreddit_name)
    await page.get_by_role("option", name=subreddit_name).click()
    await page.get_by_role("textbox", name=re.compile(r"title", re.IGNORECASE)).fill(post_title)
    await page.get_by_role("textbox", name=re.compile(r"text|body", re.IGNORECASE)).fill(post_text)
    await page.get_by_role("button", name=re.compile(r"post|submit", re.IGNORECASE)).click()


# ============================================================================
# DATA EXTRACTION SKILLS
# ============================================================================

async def get_latest_post_author(page, forum_name):
    """
    Get the author of the latest post in a forum.
    
    Args:
        page: The Playwright page object.
        forum_name: Name of the forum to check.
    
    Usage Log:
    - Extract author information from most recent post
    - Useful for tasks analyzing user activity
    - Updated to handle Postmill's author link structure (direct username links)
    """
    await page.goto(f"/f/{forum_name}")
    
    # Get first article (latest post)
    first_post = page.get_by_role("article").first
    
    # In Postmill, author links are just the username with /user/{username} URLs
    # Find the link element that points to /user/
    author_link = first_post.locator('a[href^="/user/"]').first
    author_text = await author_link.text_content()
    
    return author_text.strip()


async def get_user_comments(page, username):
    """
    Navigate to user profile and access their comments.
    
    Args:
        page: The Playwright page object.
        username: Username to get comments for.
    
    Usage Log:
    - Access user's comment history for analysis
    - Navigate to comments tab on profile
    """
    import re
    
    await page.goto(f"/user/{username}")
    
    # Click on comments tab/link
    await page.get_by_role("link", name=re.compile(r"comments", re.IGNORECASE)).click()


async def get_comment_vote_counts(page, comment_element):
    """
    Extract upvote and downvote counts from a comment element.
    
    Args:
        page: The Playwright page object.
        comment_element: Playwright locator for the comment.
    
    Usage Log:
    - Parse vote counts to compare upvotes vs downvotes
    - Returns tuple of (upvotes, downvotes)
    - Handles various vote display formats in Postmill
    """
    import re
    
    # Try to get vote count text from various possible locations
    try:
        # Look for vote/score information in the comment metadata
        vote_text = await comment_element.inner_text()
        
        # Extract all numbers from the text
        numbers = re.findall(r'(\d+)\s*point|(\d+)\s*vote|score[:\s]+(\d+)', vote_text.lower())
        
        # Flatten and filter out empty matches
        numbers = [int(n) for group in numbers for n in group if n]
        
        if len(numbers) >= 2:
            return (int(numbers[0]), int(numbers[1]))
        elif len(numbers) == 1:
            # If only one number, assume it's net score
            return (int(numbers[0]), 0)
    except:
        pass
    
    return (0, 0)


async def count_all_comments(page):
    """
    Count all comment articles on current page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Count total comments visible
    - Useful for pagination and analysis tasks
    """
    comments = page.get_by_role("article").filter(has=page.get_by_role("button", name=re.compile(r"reply", re.IGNORECASE)))
    return await comments.count()


async def navigate_to_user_comments_from_profile(page, username):
    """
    Complete workflow to view a user's comments.
    
    Composite skill that navigates to profile and accesses comments section.
    
    Args:
        page: The Playwright page object.
        username: Username to view comments for.
    
    Usage Log:
    - Full workflow for comment analysis tasks
    - Combines navigation and tab selection
    - Handles Postmill's user profile structure
    """
    import re
    
    await page.goto(f"/user/{username}")
    
    # Look for comments or submissions link/tab
    try:
        await page.get_by_role("link", name=re.compile(r"comments", re.IGNORECASE)).click()
    except:
        # If no comments link, user might not have comments or page structure is different
        pass


async def count_downvoted_comments(page, username):
    """
    Count how many comments a user has with more downvotes than upvotes.
    
    Navigates to user's comments and analyzes vote patterns.
    
    Args:
        page: The Playwright page object.
        username: Username to analyze.
    
    Usage Log:
    - Analyze user engagement patterns
    - Identify controversial comments
    """
    import re
    
    await page.goto(f"/user/{username}")
    
    # Try to navigate to comments section
    try:
        await page.get_by_role("link", name=re.compile(r"comments", re.IGNORECASE)).click()
    except:
        pass
    
    # Get all comment articles
    comments = await page.get_by_role("article").all()
    
    downvoted_count = 0
    
    for comment in comments:
        try:
            # Get the text content of the comment article
            text = await comment.inner_text()
            
            # Look for vote patterns like "X points" or upvote/downvote counts
            # In Postmill, negative scores indicate more downvotes
            score_match = re.search(r'(-?\d+)\s*point', text)
            if score_match:
                score = int(score_match.group(1))
                if score < 0:
                    downvoted_count += 1
        except:
            continue
    
    return downvoted_count
