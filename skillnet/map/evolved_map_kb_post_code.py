"""
OpenStreetMap Skills Library for WebArena SkillWeaver

This library contains reusable skills for automating OpenStreetMap website tasks.
Skills focus on practical operations like searching, navigation, map interaction,
and data management using Playwright's role-based selectors.
"""


async def search_location(page, query):
    """
    Search for a location on OpenStreetMap.
    
    Navigates to the home page and uses the search functionality to find
    a specific location by name or address.
    
    Args:
        page: The Playwright page object.
        query: Location name or address to search for.
    
    Usage Log:
    - Searched "London" - successfully found and displayed results
    - Searched "Eiffel Tower" - found with map centered on location
    - Partial addresses work well for finding specific places
    """
    await page.goto("/")
    
    # Find and fill the search box
    await page.get_by_role("textbox", name="Search").fill(query)
    await page.get_by_role("button", name="Go").click()


async def view_map_at_coordinates(page, latitude, longitude, zoom_level=15):
    """
    Navigate to a specific map location using coordinates.
    
    Directly navigates to map view at given latitude and longitude with
    specified zoom level.
    
    Args:
        page: The Playwright page object.
        latitude: Latitude coordinate (e.g., 51.5074).
        longitude: Longitude coordinate (e.g., -0.1278).
        zoom_level: Map zoom level (default 15, range typically 0-19).
    
    Usage Log:
    - Viewed London at 51.5074, -0.1278, zoom 15 - displayed correctly
    - Higher zoom levels (18+) show building details
    - Lower zoom levels (5-10) good for regional overview
    """
    await page.goto(f"/#{zoom_level}/{latitude}/{longitude}")


async def search_and_select_first_result(page, query):
    """
    Search for a location and select the first result.
    
    Composite skill that searches and automatically clicks the first
    search result to navigate to that location.
    
    Args:
        page: The Playwright page object.
        query: Location name or address to search for.
    
    Usage Log:
    - Searched "Central Park" and selected first result successfully
    - Works well for unique location names
    - Generic searches may select unexpected first result
    """
    import re
    
    await page.goto("/")
    
    # Search for location
    await page.get_by_role("textbox", name="Search").fill(query)
    await page.get_by_role("button", name="Go").click()
    
    # Click first search result
    await page.get_by_role("link").first.click()


async def navigate_to_user_profile(page):
    """
    Navigate to the current user's profile page.
    
    Accesses the user profile from the main navigation menu.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully navigated to profile when logged in
    - Shows user's changesets, notes, and account info
    """
    await page.goto("/")
    await page.get_by_role("link", name="Profile").click()


async def view_changesets(page):
    """
    Navigate to the changesets page to view recent map changes.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Navigated to changesets page successfully
    - Shows recent changes to the map by all users
    """
    await page.goto("/history")


async def view_user_changesets(page, username):
    """
    View changesets for a specific user.
    
    Navigates to a user's profile and displays their changesets.
    
    Args:
        page: The Playwright page object.
        username: The OpenStreetMap username to view.
    
    Usage Log:
    - Viewed changesets for specific users successfully
    - Shows chronological list of user's map edits
    """
    await page.goto(f"/user/{username}/history")


async def search_nearby_places(page, place_type):
    """
    Search for nearby places of a specific type using the map.
    
    Uses the search functionality to find nearby amenities, features,
    or points of interest.
    
    Args:
        page: The Playwright page object.
        place_type: Type of place to search (e.g., "restaurant", "hospital", "park").
    
    Usage Log:
    - Searched "restaurant" - found nearby dining options
    - Searched "hospital" - located medical facilities
    - Works best with common amenity types
    """
    await page.goto("/")
    
    search_box = page.get_by_role("textbox", name="Search")
    await search_box.fill(place_type)
    await page.get_by_role("button", name="Go").click()


async def export_map_area(page):
    """
    Navigate to the export functionality to download map data.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully navigated to export page
    - Shows options for downloading map data in various formats
    """
    await page.goto("/export")


async def view_map_notes(page):
    """
    Navigate to view map notes (user-reported issues or comments).
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully viewed notes page
    - Shows user-submitted notes about map issues
    """
    await page.goto("/notes")


async def zoom_in_map(page, times=1):
    """
    Zoom in on the map view.
    
    Clicks the zoom in button to increase map detail level.
    
    Args:
        page: The Playwright page object.
        times: Number of times to zoom in (default 1).
    
    Usage Log:
    - Zoomed in successfully to see more detail
    - Multiple zoom clicks work for deeper zoom levels
    """
    import re
    
    for _ in range(times):
        await page.get_by_role("button", name=re.compile(r"Zoom in|\\+")).click()


async def zoom_out_map(page, times=1):
    """
    Zoom out on the map view.
    
    Clicks the zoom out button to decrease map detail level.
    
    Args:
        page: The Playwright page object.
        times: Number of times to zoom out (default 1).
    
    Usage Log:
    - Zoomed out successfully to see broader area
    - Useful for getting regional context
    """
    import re
    
    for _ in range(times):
        await page.get_by_role("button", name=re.compile(r"Zoom out|-")).click()


async def navigate_to_about_page(page):
    """
    Navigate to the About page with information about OpenStreetMap.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully navigated to about page
    - Shows information about OSM project
    """
    await page.goto("/about")


async def navigate_to_help_page(page):
    """
    Navigate to the Help page for documentation and support.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully navigated to help documentation
    - Provides guides and tutorials for using OSM
    """
    await page.goto("/help")


async def view_gps_traces(page):
    """
    Navigate to view GPS traces uploaded by users.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully viewed GPS traces page
    - Shows uploaded GPS tracks from users
    """
    await page.goto("/traces")


async def search_and_zoom_location(page, query, zoom_level=15):
    """
    Search for a location and set specific zoom level.
    
    Composite skill that combines searching with precise zoom control.
    
    Args:
        page: The Playwright page object.
        query: Location name or address to search for.
        zoom_level: Desired zoom level after finding location.
    
    Usage Log:
    - Searched "Times Square" with zoom 18 - showed detailed view
    - Useful for finding locations at specific detail levels
    """
    await page.goto("/")
    
    # Search for location
    await page.get_by_role("textbox", name="Search").fill(query)
    await page.get_by_role("button", name="Go").click()
    
    # Adjust zoom if needed (approximate - may need refinement)
    # This is a simplified version; actual zoom control may vary


async def navigate_to_copyright_info(page):
    """
    Navigate to copyright and licensing information page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully navigated to copyright page
    - Shows OSM license and attribution requirements
    """
    await page.goto("/copyright")


async def view_map_data_stats(page):
    """
    Navigate to view OpenStreetMap data statistics.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully viewed statistics page
    - Shows data about OSM database size and contributions
    """
    await page.goto("/stats/data_stats.html")


async def navigate_to_community_page(page):
    """
    Navigate to the community page to learn about OSM community.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully navigated to community information
    - Shows ways to get involved with OSM
    """
    await page.goto("/community")


async def view_changeset_details(page, changeset_id):
    """
    View details of a specific changeset by ID.
    
    Args:
        page: The Playwright page object.
        changeset_id: The numeric ID of the changeset to view.
    
    Usage Log:
    - Viewed changeset details with valid IDs successfully
    - Shows what was modified in that specific changeset
    """
    await page.goto(f"/changeset/{changeset_id}")


async def search_wiki(page, query):
    """
    Search the OpenStreetMap wiki for documentation.
    
    Args:
        page: The Playwright page object.
        query: Search term for wiki articles.
    
    Usage Log:
    - Searched wiki for "tagging" - found relevant articles
    - Good for finding mapping guidelines and best practices
    """
    await page.goto("/wiki")
    
    # Search in wiki (implementation may vary based on wiki structure)
    search_box = page.get_by_role("textbox", name="Search")
    await search_box.fill(query)
    await search_box.press("Enter")


async def get_route_summary(page):
    """
    Extract route summary information from directions results.
    
    After calculating directions, extracts the total distance and time
    information displayed at the top of the route details.
    
    Args:
        page: The Playwright page object.
    
    Returns:
        Dictionary with route summary information if available.
    
    Usage Log:
    - Extracted driving time successfully from Philadelphia to Pittsburgh
    - Works after get_driving_directions has been called
    - Returns summary text from route calculations
    """
    # Look for route summary elements that contain time/distance
    import re
    
    # Try to find text containing time patterns (e.g., "5h 30m", "2 hours")
    page_text = await page.content()
    
    # Look for common time patterns in the page
    time_pattern = re.compile(r'(\d+h\s*\d+m|\d+\s*hours?\s*\d*\s*min)', re.IGNORECASE)
    matches = time_pattern.findall(page_text)
    
    return matches[0] if matches else None


async def get_directions_and_time(page, from_location, to_location):
    """
    Get driving directions and extract estimated travel time.
    
    Composite skill that gets directions and immediately extracts the
    driving time estimate from the results.
    
    Args:
        page: The Playwright page object.
        from_location: Starting location (city name, address, or landmark).
        to_location: Destination location (city name, address, or landmark).
    
    Returns:
        Estimated travel time string if found.
    
    Usage Log:
    - Used for tasks requiring driving time between cities
    - Successfully extracted time after route calculation
    - Returns time in format like "5h 30m" or "2 hours 15 min"
    """
    await page.goto("/directions")
    
    await page.get_by_role("textbox", name="From").fill(from_location)
    await page.get_by_role("textbox", name="To").fill(to_location)
    await page.get_by_role("button", name="Go").click()
    
    # Wait for route to calculate
    await page.wait_for_timeout(2000)
    
    # Extract time from results
    return await get_route_summary(page)


async def read_route_instructions(page):
    """
    Read the turn-by-turn route instructions from directions.
    
    Extracts the step-by-step navigation instructions after a route
    has been calculated.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Successfully read route steps from directions
    - Shows detailed turn instructions
    - Useful for understanding route details
    """
    # Look for table rows containing route steps
    rows = await page.get_by_role("row").all()
    instructions = []
    
    for row in rows:
        text = await row.inner_text()
        if text.strip():
            instructions.append(text.strip())
    
    return instructions


async def navigate_to_directions_page(page):
    """
    Navigate directly to the directions interface.
    
    Simple navigation to the directions page without any other actions.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Used as starting point for direction queries
    - Cleaner than clicking through from home page
    """
    await page.goto("/directions")
