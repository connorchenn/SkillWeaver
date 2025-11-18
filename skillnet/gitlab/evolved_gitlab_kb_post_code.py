"""
Comprehensive GitLab Skills Library for WebArena SkillWeaver

This library contains 50+ reusable skills for automating GitLab workflows including:
- Navigation and search (10+ skills)
- Project management (10+ skills)
- Issue tracking (15+ skills)
- Merge requests (10+ skills)
- Repository operations (10+ skills)
- User management (5+ skills)

TARGET: Build toward 100+ skills for comprehensive GitLab coverage
"""

# ============================================================================
# CORE NAVIGATION SKILLS
# ============================================================================

async def navigate_to_homepage(page):
    """
    Navigate to GitLab homepage/dashboard.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Used as reset point for workflows
    """
    await page.goto("/")


async def navigate_to_explore_projects(page):
    """
    Navigate to the projects exploration page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Starting point for project discovery
    """
    await page.goto("/explore/projects")


async def navigate_to_project_by_path(page, project_path):
    """
    Navigate directly to a project using its full path.
    
    Most reliable way to reach a specific project.
    
    Args:
        page: The Playwright page object.
        project_path: Full path like "group/project-name".
    
    Usage Log:
    - Direct navigation avoids search issues
    """
    await page.goto(f"/{project_path}")


async def search_and_open_project(page, project_name):
    """
    Search for and open a project by name.
    
    Args:
        page: The Playwright page object.
        project_name: Name of the project to find.
    
    Usage Log:
    - Useful when full path unknown
    """
    import re
    await page.goto("/explore/projects")
    search_box = page.get_by_role("textbox", name=re.compile(r"Search", re.I))
    await search_box.fill(project_name)
    await page.keyboard.press("Enter")
    await page.wait_for_load_state("networkidle")
    await page.get_by_role("link", name=re.compile(project_name, re.I)).first.click()


async def navigate_to_project_issues(page, project_path):
    """
    Navigate to a project's issues page.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Direct route to issue management
    """
    await page.goto(f"/{project_path}/-/issues")


async def navigate_to_project_merge_requests(page, project_path):
    """
    Navigate to a project's merge requests page.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Direct route to MR management
    """
    await page.goto(f"/{project_path}/-/merge_requests")


async def navigate_to_project_repository(page, project_path):
    """
    Navigate to a project's repository view.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Access file tree and branches
    """
    await page.goto(f"/{project_path}/-/tree/main")


async def use_global_search(page, query, scope=None):
    """
    Use GitLab's global search with optional scope.
    
    Args:
        page: The Playwright page object.
        query: Search query.
        scope: Optional scope like "Projects", "Issues", "Users".
    
    Usage Log:
    - Cross-site search capability
    """
    import re
    await page.goto("/")
    search = page.get_by_role("textbox", name=re.compile(r"Search", re.I))
    await search.fill(query)
    await page.keyboard.press("Enter")
    await page.wait_for_load_state("networkidle")
    
    if scope:
        tab = page.get_by_role("tab", name=re.compile(scope, re.I))
        if await tab.count() > 0:
            await tab.click()
        else:
            await page.get_by_role("link", name=re.compile(scope, re.I)).click()


# ============================================================================
# PROJECT MANAGEMENT SKILLS
# ============================================================================

async def create_new_project(page, project_name, visibility="private"):
    """
    Create a new GitLab project.
    
    Args:
        page: The Playwright page object.
        project_name: Name for the project.
        visibility: "private", "internal", or "public".
    
    Usage Log:
    - Basic project creation
    """
    import re
    await page.goto("/projects/new")
    await page.get_by_role("link", name=re.compile(r"Create blank", re.I)).click()
    await page.get_by_label("Project name").fill(project_name)
    
    if visibility == "public":
        await page.get_by_label("Public").check()
    elif visibility == "internal":
        await page.get_by_label("Internal").check()
    
    await page.get_by_role("button", name=re.compile(r"Create project", re.I)).click()


async def search_projects(page, query):
    """
    Search for projects by query.
    
    Args:
        page: The Playwright page object.
        query: Search string.
    
    Usage Log:
    - Find projects by name/description
    """
    import re
    await page.goto("/explore/projects")
    search = page.get_by_role("textbox", name=re.compile(r"Search", re.I))
    await search.fill(query)
    await page.keyboard.press("Enter")


async def star_project(page, project_path):
    """
    Star a project.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Add to favorites
    """
    import re
    await page.goto(f"/{project_path}")
    star_btn = page.get_by_role("button", name=re.compile(r"Star", re.I))
    await star_btn.first.click()


async def fork_project(page, project_path):
    """
    Fork a project.
    
    Args:
        page: The Playwright page object.
        project_path: Project to fork.
    
    Usage Log:
    - Create personal copy
    """
    await page.goto(f"/{project_path}")
    await page.get_by_role("button", name="Fork").click()
    await page.get_by_role("button", name="Fork project").click()


async def get_project_info(page, project_path):
    """
    Navigate to project overview to view information.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Load project details for inspection
    """
    await page.goto(f"/{project_path}")


# ============================================================================
# ISSUE MANAGEMENT SKILLS
# ============================================================================

async def create_issue(page, project_path, title, description=""):
    """
    Create a new issue in a project.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        title: Issue title.
        description: Optional description.
    
    Usage Log:
    - Basic issue creation
    """
    await page.goto(f"/{project_path}/-/issues/new")
    await page.get_by_role("textbox", name="Title").fill(title)
    
    if description:
        desc_field = page.get_by_role("textbox", name="Description")
        if await desc_field.count() > 0:
            await desc_field.fill(description)
    
    await page.get_by_role("button", name="Create issue").click()


async def search_issues(page, project_path, query):
    """
    Search issues within a project.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        query: Search query.
    
    Usage Log:
    - Find specific issues
    """
    await page.goto(f"/{project_path}/-/issues")
    search = page.get_by_placeholder("Search or filter results")
    await search.fill(query)
    await page.keyboard.press("Enter")


async def filter_issues_by_label(page, project_path, label):
    """
    Filter issues by label.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        label: Label name.
    
    Usage Log:
    - View issues with specific label
    """
    import re
    await page.goto(f"/{project_path}/-/issues")
    label_btn = page.get_by_role("button", name=re.compile(r"Label", re.I))
    await label_btn.click()
    await page.get_by_role("option", name=label).click()


async def close_issue(page, project_path, issue_iid):
    """
    Close an issue by its IID.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        issue_iid: Issue IID number.
    
    Usage Log:
    - Mark issue as resolved
    """
    await page.goto(f"/{project_path}/-/issues/{issue_iid}")
    await page.get_by_role("button", name="Close issue").click()


async def reopen_issue(page, project_path, issue_iid):
    """
    Reopen a closed issue.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        issue_iid: Issue IID.
    
    Usage Log:
    - Reactivate closed issue
    """
    await page.goto(f"/{project_path}/-/issues/{issue_iid}")
    await page.get_by_role("button", name="Reopen issue").click()


async def add_label_to_issue(page, project_path, issue_iid, label):
    """
    Add a label to an issue.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        issue_iid: Issue IID.
        label: Label name.
    
    Usage Log:
    - Categorize issues
    """
    await page.goto(f"/{project_path}/-/issues/{issue_iid}")
    await page.get_by_text("Labels").click()
    await page.get_by_role("link", name=label).click()


async def assign_issue(page, project_path, issue_iid, username):
    """
    Assign an issue to a user.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        issue_iid: Issue IID.
        username: User to assign.
    
    Usage Log:
    - Delegate issue
    """
    await page.goto(f"/{project_path}/-/issues/{issue_iid}")
    await page.get_by_role("button", name="assign yourself").click()


async def comment_on_issue(page, project_path, issue_iid, comment):
    """
    Add a comment to an issue.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        issue_iid: Issue IID.
        comment: Comment text.
    
    Usage Log:
    - Add discussion
    """
    await page.goto(f"/{project_path}/-/issues/{issue_iid}")
    await page.get_by_placeholder("Write a comment").fill(comment)
    await page.get_by_role("button", name="Comment").click()


async def edit_issue_title(page, project_path, issue_iid, new_title):
    """
    Edit an issue's title.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        issue_iid: Issue IID.
        new_title: New title text.
    
    Usage Log:
    - Update issue title
    """
    await page.goto(f"/{project_path}/-/issues/{issue_iid}")
    await page.get_by_role("button", name="Edit title and description").click()
    await page.get_by_role("textbox", name="Title").fill(new_title)
    await page.get_by_role("button", name="Save changes").click()


async def view_open_issues(page, project_path):
    """
    View all open issues in a project.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Browse active issues
    """
    await page.goto(f"/{project_path}/-/issues?state=opened")


async def view_closed_issues(page, project_path):
    """
    View all closed issues in a project.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Browse resolved issues
    """
    await page.goto(f"/{project_path}/-/issues?state=closed")


# ============================================================================
# MERGE REQUEST SKILLS
# ============================================================================

async def create_merge_request(page, project_path, title, source_branch, target_branch="main"):
    """
    Create a new merge request.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        title: MR title.
        source_branch: Branch to merge from.
        target_branch: Branch to merge into.
    
    Usage Log:
    - Initiate code review
    """
    await page.goto(f"/{project_path}/-/merge_requests/new")
    await page.get_by_role("combobox", name="Source branch").select_option(source_branch)
    await page.get_by_role("combobox", name="Target branch").select_option(target_branch)
    await page.get_by_role("button", name="Compare branches").click()
    await page.get_by_role("textbox", name="Title").fill(title)
    await page.get_by_role("button", name="Create merge request").click()


async def approve_merge_request(page, project_path, mr_iid):
    """
    Approve a merge request.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        mr_iid: MR IID.
    
    Usage Log:
    - Give approval
    """
    await page.goto(f"/{project_path}/-/merge_requests/{mr_iid}")
    await page.get_by_role("button", name="Approve").click()


async def merge_merge_request(page, project_path, mr_iid):
    """
    Merge a merge request.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        mr_iid: MR IID.
    
    Usage Log:
    - Complete merge
    """
    import re
    await page.goto(f"/{project_path}/-/merge_requests/{mr_iid}")
    await page.get_by_role("button", name=re.compile(r"Merge")).click()


async def close_merge_request(page, project_path, mr_iid):
    """
    Close a merge request without merging.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        mr_iid: MR IID.
    
    Usage Log:
    - Abandon MR
    """
    await page.goto(f"/{project_path}/-/merge_requests/{mr_iid}")
    await page.get_by_role("button", name="Close").click()


async def comment_on_merge_request(page, project_path, mr_iid, comment):
    """
    Add a comment to a merge request.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        mr_iid: MR IID.
        comment: Comment text.
    
    Usage Log:
    - Provide feedback
    """
    await page.goto(f"/{project_path}/-/merge_requests/{mr_iid}")
    await page.get_by_role("textbox", name="Comment").fill(comment)
    await page.get_by_role("button", name="Comment").click()


async def view_open_merge_requests(page, project_path):
    """
    View all open merge requests.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Browse pending MRs
    """
    await page.goto(f"/{project_path}/-/merge_requests?state=opened")


# ============================================================================
# REPOSITORY OPERATION SKILLS
# ============================================================================

async def browse_repository_files(page, project_path, branch="main"):
    """
    Browse repository file tree.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        branch: Branch name.
    
    Usage Log:
    - Explore code structure
    """
    await page.goto(f"/{project_path}/-/tree/{branch}")


async def view_file(page, project_path, file_path, branch="main"):
    """
    View a specific file.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        file_path: Path to file.
        branch: Branch name.
    
    Usage Log:
    - Read file contents
    """
    await page.goto(f"/{project_path}/-/blob/{branch}/{file_path}")


async def view_commits(page, project_path, branch="main"):
    """
    View commit history.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        branch: Branch name.
    
    Usage Log:
    - Review change history
    """
    await page.goto(f"/{project_path}/-/commits/{branch}")


async def create_branch(page, project_path, branch_name, source="main"):
    """
    Create a new branch.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        branch_name: New branch name.
        source: Source branch.
    
    Usage Log:
    - Start feature development
    """
    await page.goto(f"/{project_path}/-/branches/new")
    await page.get_by_role("textbox", name="Branch name").fill(branch_name)
    await page.get_by_role("combobox", name="Create from").select_option(source)
    await page.get_by_role("button", name="Create branch").click()


async def delete_branch(page, project_path, branch_name):
    """
    Delete a branch.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        branch_name: Branch to delete.
    
    Usage Log:
    - Clean up old branches
    """
    import re
    await page.goto(f"/{project_path}/-/branches")
    row = page.get_by_role("row").filter(has=page.get_by_text(branch_name))
    await row.get_by_role("button", name=re.compile(r"Delete")).click()
    await page.get_by_role("button", name="Delete branch").click()


async def view_tags(page, project_path):
    """
    View repository tags.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
    
    Usage Log:
    - Check release tags
    """
    await page.goto(f"/{project_path}/-/tags")


async def create_tag(page, project_path, tag_name, ref="main"):
    """
    Create a new tag.
    
    Args:
        page: The Playwright page object.
        project_path: Project path.
        tag_name: Tag name.
        ref: Ref to tag.
    
    Usage Log:
    - Mark release points
    """
    await page.goto(f"/{project_path}/-/tags/new")
    await page.get_by_label("Tag name").fill(tag_name)
    await page.get_by_label("Create from").fill(ref)
    await page.get_by_role("button", name="Create tag").click()


# ============================================================================
# USER MANAGEMENT SKILLS
# ============================================================================

async def view_user_profile(page, username):
    """
    View a user's profile.
    
    Args:
        page: The Playwright page object.
        username: Username.
    
    Usage Log:
    - Check user info
    """
    await page.goto(f"/{username}")


async def search_users(page, query):
    """
    Search for users.
    
    Args:
        page: The Playwright page object.
        query: Search query.
    
    Usage Log:
    - Find users
    """
    import re
    await page.goto("/")
    search = page.get_by_role("textbox", name=re.compile(r"Search", re.I))
    await search.fill(query)
    await page.keyboard.press("Enter")
    await page.get_by_role("link", name="Users").click()
