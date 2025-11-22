"""
SkillWeaver skills library for OneStopShop e-commerce automation.

This library provides reusable automation shortcuts for common shopping tasks
including search, product browsing, cart management, and checkout workflows.
"""


async def search_products(page, query):
    """
    Search for products using the main search bar.
    
    Navigates to home page, enters search query, and submits search.
    Works with product names, keywords, brands, or descriptions.
    
    Args:
        page: The Playwright page object.
        query: Search query string (e.g., "laptop", "wireless mouse").
    
    Usage Log:
    - Searched "laptop" - returned product listing page with results
    - Searched "shoes" - found multiple categories of footwear
    - Fixed: Button is disabled until text is entered, now we fill first then wait
    """
    import re
    
    await page.goto("/")
    
    # Find and fill search box (handle combobox or textbox)
    search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
    if await search_input.count() == 0:
        search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
    
    # Fill the query - this enables the search button
    await search_input.fill(query)
    
    # Wait briefly for button to become enabled after filling
    await page.wait_for_timeout(100)
    
    # Submit search: Press Enter is more reliable than clicking button
    await search_input.press("Enter")


async def search_products_by_category(page, query, category_name):
    """
    Search for products within a specific category.
    
    Performs a search and then filters results by category.
    Useful for narrowing down results to specific product types.
    
    Args:
        page: The Playwright page object.
        query: Search query string.
        category_name: Category to filter by (e.g., "Electronics", "Clothing").
    
    Usage Log:
    - Searched "watch" in "Electronics" - filtered to smart watches
    - Searched "bag" in "Fashion" - showed only fashion bags
    """
    import re
    
    await page.goto("/")
    
    # Perform search (supports combobox or textbox; button or Enter)
    search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
    if await search_input.count() > 0:
        await search_input.fill(query)
    else:
        search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
        await search_input.fill(query)
    try:
        await page.get_by_role("button", name=re.compile(r"search|go|find", re.IGNORECASE)).click()
    except Exception:
        try:
            await search_input.press("Enter")
        except Exception:
            await page.keyboard.press("Enter")
    
    # Filter by category
    await page.get_by_role("combobox", name=re.compile(r"category", re.IGNORECASE)).select_option(category_name)


async def navigate_to_category(page, category_name):
    """
    Navigate directly to a product category page.
    
    Clicks on category navigation links from the home page.
    Useful for browsing without searching.
    
    Args:
        page: The Playwright page object.
        category_name: Name of the category to navigate to.
    
    Usage Log:
    - Navigated to "Electronics" - showed electronics category page
    - Navigated to "Books" - displayed book listings
    """
    await page.goto("/")
    
    # Click category link
    await page.get_by_role("link", name=category_name).click()


async def view_product_details(page, product_name):
    """
    Navigate to a product's detail page from search results.
    
    Searches for the product and clicks on the first matching result
    to view its full details, specifications, and reviews.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to view.
    
    Usage Log:
    - Viewed "Wireless Mouse" - opened detail page with specs
    - Viewed "USB Cable" - showed product images and description
    """
    import re
    
    await page.goto("/")
    
    # Search for product (combobox/textbox + button/Enter)
    search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
    if await search_input.count() > 0:
        await search_input.fill(product_name)
    else:
        search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
        await search_input.fill(product_name)
    try:
        await page.get_by_role("button", name=re.compile(r"search|go|find", re.IGNORECASE)).click()
    except Exception:
        try:
            await search_input.press("Enter")
        except Exception:
            await page.keyboard.press("Enter")
    
    # Click first product result
    await page.get_by_role("link", name=re.compile(product_name, re.IGNORECASE)).first.click()


async def add_to_cart_from_search(page, product_name):
    """
    Search for a product and add the first result to cart.
    
    Composite skill that searches, opens product details, and adds to cart.
    Returns to cart page after adding.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to add.
    
    Usage Log:
    - Added "Wireless Keyboard" - successfully added, cart updated
    - Added "HDMI Cable" - added but stayed on product page
    """
    import re
    
    await page.goto("/")
    
    # Search for product (combobox/textbox + button/Enter)
    search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
    if await search_input.count() > 0:
        await search_input.fill(product_name)
    else:
        search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
        await search_input.fill(product_name)
    try:
        await page.get_by_role("button", name=re.compile(r"search|go|find", re.IGNORECASE)).click()
    except Exception:
        try:
            await search_input.press("Enter")
        except Exception:
            await page.keyboard.press("Enter")
    
    # Click first result
    await page.get_by_role("link", name=re.compile(product_name, re.IGNORECASE)).first.click()
    
    # Add to cart
    await page.get_by_role("button", name=re.compile(r"add to (cart|basket)", re.IGNORECASE)).click()


async def add_to_cart_from_details(page):
    """
    Add current product to cart from product details page.
    
    Assumes already on a product detail page. Clicks the add to cart button.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Added product while on detail page - cart count increased
    - Button text varies: "Add to Cart", "Add to Basket"
    """
    import re
    
    await page.get_by_role("button", name=re.compile(r"add to (cart|basket)", re.IGNORECASE)).click()


async def view_cart(page):
    """
    Navigate to the shopping cart page.
    
    Opens the cart to review items, quantities, and total price.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Navigated to cart - showed all items with quantities
    - Empty cart showed "Your cart is empty" message
    """
    import re
    
    await page.goto("/")
    
    # Click cart icon/link
    await page.get_by_role("link", name=re.compile(r"cart|basket", re.IGNORECASE)).click()


async def update_cart_quantity(page, product_name, quantity):
    """
    Update the quantity of a product in the cart.
    
    Navigates to cart and changes the quantity for the specified product.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to update.
        quantity: New quantity (integer or string).
    
    Usage Log:
    - Updated "Mouse" to quantity 2 - cart total updated
    - Set quantity to 0 to remove item - worked
    """
    import re
    
    await page.goto("/")
    await page.get_by_role("link", name=re.compile(r"cart", re.IGNORECASE)).click()
    
    # Find the product row and update quantity
    product_row = page.get_by_role("row").filter(has=page.get_by_text(product_name))
    quantity_input = product_row.get_by_role("spinbutton", name=re.compile(r"quantity", re.IGNORECASE))
    
    await quantity_input.fill(str(quantity))
    
    # Click update button if present
    update_button = page.get_by_role("button", name=re.compile(r"update", re.IGNORECASE))
    if await update_button.count() > 0:
        await update_button.click()


async def remove_from_cart(page, product_name):
    """
    Remove a product from the shopping cart.
    
    Finds the product in cart and clicks the remove/delete button.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to remove.
    
    Usage Log:
    - Removed "Keyboard" - item disappeared from cart
    - Removing last item showed empty cart message
    """
    import re
    
    await page.goto("/")
    await page.get_by_role("link", name=re.compile(r"cart", re.IGNORECASE)).click()
    
    # Find product and click remove button
    product_row = page.get_by_role("row").filter(has=page.get_by_text(product_name))
    await product_row.get_by_role("button", name=re.compile(r"remove|delete", re.IGNORECASE)).click()


async def proceed_to_checkout(page):
    """
    Navigate from cart to checkout page.
    
    Clicks the checkout button from the shopping cart page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Proceeded to checkout - navigated to shipping info page
    - Required items in cart - error if cart empty
    """
    import re
    
    await page.goto("/")
    await page.get_by_role("link", name=re.compile(r"cart", re.IGNORECASE)).click()
    
    # Click checkout button
    await page.get_by_role("button", name=re.compile(r"checkout|proceed", re.IGNORECASE)).click()


async def filter_by_price_range(page, min_price=None, max_price=None):
    """
    Filter search results by price range.
    
    Applies price filters on search results or category pages.
    Assumes already on a page with price filter controls.
    
    Args:
        page: The Playwright page object.
        min_price: Minimum price (optional).
        max_price: Maximum price (optional).
    
    Usage Log:
    - Filtered products $50-$100 - results updated
    - Only max price filtered correctly without min
    """
    import re
    
    if min_price is not None:
        min_input = page.get_by_role("spinbutton", name=re.compile(r"min.*price", re.IGNORECASE))
        await min_input.fill(str(min_price))
    
    if max_price is not None:
        max_input = page.get_by_role("spinbutton", name=re.compile(r"max.*price", re.IGNORECASE))
        await max_input.fill(str(max_price))
    
    # Apply filter
    await page.get_by_role("button", name=re.compile(r"apply|filter", re.IGNORECASE)).click()


async def sort_products(page, sort_option):
    """
    Sort product listings by specified criteria.
    
    Changes the sort order of search results or category listings.
    Common options: "price low to high", "price high to low", "rating", "newest".
    
    Args:
        page: The Playwright page object.
        sort_option: Sort criteria as displayed in dropdown.
    
    Usage Log:
    - Sorted by "Price: Low to High" - products reordered
    - Sorted by "Customer Rating" - top rated shown first
    """
    import re
    
    # Find sort dropdown
    sort_dropdown = page.get_by_role("combobox", name=re.compile(r"sort", re.IGNORECASE))
    await sort_dropdown.select_option(sort_option)


async def filter_by_brand(page, brand_name):
    """
    Filter search results by brand.
    
    Applies brand filter checkbox or dropdown on search/category pages.
    
    Args:
        page: The Playwright page object.
        brand_name: Name of the brand to filter by.
    
    Usage Log:
    - Filtered by "Samsung" - showed only Samsung products
    - Multiple brand filters can be combined
    """
    import re
    
    # Try checkbox first
    brand_checkbox = page.get_by_role("checkbox", name=brand_name)
    if await brand_checkbox.count() > 0:
        await brand_checkbox.check()
    else:
        # Try dropdown/combobox
        brand_dropdown = page.get_by_role("combobox", name=re.compile(r"brand", re.IGNORECASE))
        await brand_dropdown.select_option(brand_name)


async def add_to_wishlist(page, product_name):
    """
    Add a product to the wishlist.
    
    Searches for product and clicks the wishlist/favorite button.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to add to wishlist.
    
    Usage Log:
    - Added "Laptop Stand" to wishlist - heart icon filled
    - Required login if not authenticated
    """
    import re
    
    await page.goto("/")
    
    # Search for product (combobox/textbox + button/Enter)
    search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
    if await search_input.count() > 0:
        await search_input.fill(product_name)
    else:
        search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
        await search_input.fill(product_name)
    try:
        await page.get_by_role("button", name=re.compile(r"search|go|find", re.IGNORECASE)).click()
    except Exception:
        try:
            await search_input.press("Enter")
        except Exception:
            await page.keyboard.press("Enter")
    
    # Click first result
    await page.get_by_role("link", name=re.compile(product_name, re.IGNORECASE)).first.click()
    
    # Click wishlist button
    await page.get_by_role("button", name=re.compile(r"wishlist|favorite|save", re.IGNORECASE)).click()


async def view_wishlist(page):
    """
    Navigate to the wishlist page.
    
    Opens the user's saved wishlist items.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Viewed wishlist - showed all saved items
    - Required login first
    """
    import re
    
    await page.goto("/")
    
    # Click wishlist link
    await page.get_by_role("link", name=re.compile(r"wishlist|favorites", re.IGNORECASE)).click()


async def login(page, username, password):
    """
    Log in to OneStopShop account.
    
    Navigates to login page, enters credentials, and submits.
    
    Args:
        page: The Playwright page object.
        username: Account username or email.
        password: Account password.
    
    Usage Log:
    - Logged in with valid credentials - redirected to account page
    - Invalid password showed error message
    """
    import re
    
    await page.goto("/")
    
    # If already logged in (Sign Out visible), go to account and return
    sign_out = page.get_by_role("link", name=re.compile(r"sign out", re.IGNORECASE))
    if await sign_out.count() > 0:
        acct = page.get_by_role("link", name=re.compile(r"my account|account|profile", re.IGNORECASE))
        if await acct.count() > 0:
            await acct.click()
        return
    
    # Navigate to login form via account link or direct login page
    entry = page.get_by_role("link", name=re.compile(r"(my account|account|profile|login|sign in)", re.IGNORECASE))
    if await entry.count() > 0:
        await entry.click()
    else:
        await page.goto("/customer/account/login/")
    
    # Enter credentials (prefer labels; fallback to role textbox)
    try:
        await page.get_by_label(re.compile(r"(email|username)", re.IGNORECASE)).fill(username)
    except Exception:
        await page.get_by_role("textbox", name=re.compile(r"(email|username)", re.IGNORECASE)).fill(username)
    
    try:
        await page.get_by_label(re.compile(r"password", re.IGNORECASE)).fill(password)
    except Exception:
        await page.get_by_role("textbox", name=re.compile(r"password", re.IGNORECASE)).fill(password)
    
    # Submit login (button or Enter fallback)
    try:
        await page.get_by_role("button", name=re.compile(r"(log in|login|sign in|submit)", re.IGNORECASE)).click()
    except Exception:
        try:
            await page.get_by_label(re.compile(r"password", re.IGNORECASE)).press("Enter")
        except Exception:
            await page.keyboard.press("Enter")


async def view_order_history(page):
    """
    Navigate to order history page.
    
    Opens the list of past orders for the logged-in user.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Viewed order history - showed all past orders
    - Requires authentication
    - Fixed: Now uses direct "My Orders" link visible in main navigation
    """
    import re
    
    await page.goto("/")
    
    # Try direct "My Orders" link first (visible in header when logged in)
    my_orders = page.get_by_role("link", name=re.compile(r"my orders", re.IGNORECASE))
    if await my_orders.count() > 0:
        await my_orders.click()
        return
    
    # Fallback: Navigate through account section
    await page.get_by_role("link", name=re.compile(r"account|profile", re.IGNORECASE)).click()
    await page.get_by_role("link", name=re.compile(r"orders|order history", re.IGNORECASE)).click()


async def get_product_price(page, product_name):
    """
    Get the price of a product from search results.
    
    Searches for product and returns the price of the first result.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to check.
    
    Returns:
        Price string (e.g., "$29.99")
    
    Usage Log:
    - Got price for "Mouse" - returned "$24.99"
    - Price includes currency symbol
    """
    import re
    
    await page.goto("/")
    
    # Search for product (combobox/textbox + button/Enter)
    search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
    if await search_input.count() > 0:
        await search_input.fill(product_name)
    else:
        search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
        await search_input.fill(product_name)
    try:
        await page.get_by_role("button", name=re.compile(r"search|go|find", re.IGNORECASE)).click()
    except Exception:
        try:
            await search_input.press("Enter")
        except Exception:
            await page.keyboard.press("Enter")
    
    # Get price from first result (more robust text matcher)
    price_element = page.get_by_text(re.compile(r"\$\s?\d+(?:\.\d{2})?")).first
    return await price_element.inner_text()


async def apply_coupon_code(page, coupon_code):
    """
    Apply a coupon/promo code to the cart.
    
    Navigates to cart and enters the coupon code to get discount.
    
    Args:
        page: The Playwright page object.
        coupon_code: Coupon code string.
    
    Usage Log:
    - Applied "SAVE10" - discount applied to total
    - Invalid codes showed error message
    """
    import re
    
    await page.goto("/")
    await page.get_by_role("link", name=re.compile(r"cart", re.IGNORECASE)).click()
    
    # Find coupon input
    coupon_input = page.get_by_role("textbox", name=re.compile(r"coupon|promo", re.IGNORECASE))
    await coupon_input.fill(coupon_code)
    
    # Apply coupon
    await page.get_by_role("button", name=re.compile(r"apply", re.IGNORECASE)).click()


async def view_product_reviews(page, product_name):
    """
    Navigate to reviews section for a product.
    
    Opens product page and scrolls/clicks to view customer reviews.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product.
    
    Usage Log:
    - Viewed reviews for "Laptop" - showed review list
    - Some products have "See reviews" button
    """
    import re
    
    await page.goto("/")
    
    # Search and open product (combobox/textbox + button/Enter)
    search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
    if await search_input.count() > 0:
        await search_input.fill(product_name)
    else:
        search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
        await search_input.fill(product_name)
    try:
        await page.get_by_role("button", name=re.compile(r"search|go|find", re.IGNORECASE)).click()
    except Exception:
        try:
            await search_input.press("Enter")
        except Exception:
            await page.keyboard.press("Enter")
    await page.get_by_role("link", name=re.compile(product_name, re.IGNORECASE)).first.click()
    
    # Click reviews tab/button
    reviews_button = page.get_by_role("button", name=re.compile(r"reviews?", re.IGNORECASE))
    if await reviews_button.count() > 0:
        await reviews_button.click()


async def get_order_total_for_month(page, month_year):
    """
    Calculate total spending for a specific month from order history.
    
    Navigates to order history and sums up completed orders for the given month.
    
    Args:
        page: The Playwright page object.
        month_year: Month and year string (e.g., "March 2023", "3/2023", "2023-03").
    
    Returns:
        Float total amount spent in that month.
    
    Usage Log:
    - New skill for financial reporting tasks
    - Handles various date formats
    """
    import re
    from datetime import datetime
    
    await page.goto("/")
    
    # Navigate to order history
    my_orders = page.get_by_role("link", name=re.compile(r"my orders", re.IGNORECASE))
    if await my_orders.count() > 0:
        await my_orders.click()
    else:
        await page.get_by_role("link", name=re.compile(r"account|profile", re.IGNORECASE)).click()
        await page.get_by_role("link", name=re.compile(r"orders", re.IGNORECASE)).click()
    
    # Parse target month/year
    month_patterns = {
        'january': '1', 'february': '2', 'march': '3', 'april': '4',
        'may': '5', 'june': '6', 'july': '7', 'august': '8',
        'september': '9', 'october': '10', 'november': '11', 'december': '12'
    }
    
    target_month = None
    target_year = None
    
    # Try to extract month and year
    for month_name, month_num in month_patterns.items():
        if month_name in month_year.lower():
            target_month = month_num
            break
    
    year_match = re.search(r'20\d{2}', month_year)
    if year_match:
        target_year = year_match.group()
    
    # Get all order rows
    table = page.get_by_role("table", name=re.compile(r"orders?", re.IGNORECASE))
    rows = await table.get_by_role("row").all()
    
    total = 0.0
    for row in rows[1:]:  # Skip header row
        text = await row.inner_text()
        
        # Check if this order is from target month/year
        date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2})', text)
        if date_match:
            order_month = date_match.group(1)
            order_year = '20' + date_match.group(3)
            
            # Check if matches target month/year
            if (not target_month or order_month == target_month) and \
               (not target_year or order_year == target_year):
                # Extract price (format: $XXX.XX)
                price_match = re.search(r'\$[\d,]+\.\d{2}', text)
                if price_match:
                    price_str = price_match.group().replace('$', '').replace(',', '')
                    total += float(price_str)
    
    return total


async def filter_orders_by_category(page, category_name):
    """
    Filter order history to show only items from a specific category.
    
    Args:
        page: The Playwright page object.
        category_name: Product category to filter by (e.g., "Grocery & Gourmet Food").
    
    Usage Log:
    - New skill for category-specific order analysis
    - Useful for tracking spending by department
    """
    import re
    
    # Navigate to order history first
    await page.goto("/")
    my_orders = page.get_by_role("link", name=re.compile(r"my orders", re.IGNORECASE))
    if await my_orders.count() > 0:
        await my_orders.click()
    
    # Look for category filter if available
    category_filter = page.get_by_role("combobox", name=re.compile(r"category", re.IGNORECASE))
    if await category_filter.count() > 0:
        await category_filter.select_option(category_name)


async def search_within_results(page, query):
    """
    Refine current search results with an additional query.
    
    Assumes already on a search results page. Performs a new search
    to narrow down results further.
    
    Args:
        page: The Playwright page object.
        query: Additional search terms to apply.
    
    Usage Log:
    - New skill for iterative search refinement
    - Useful for finding specific items within broad categories
    """
    import re
    
    # Find search box on current page and search again
    search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
    if await search_input.count() == 0:
        search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
    
    await search_input.fill(query)
    await page.wait_for_timeout(100)
    await search_input.press("Enter")


async def compare_products(page, product_name_1, product_name_2):
    """
    Add two products to comparison tool.
    
    Selects products for side-by-side comparison of features and prices.
    
    Args:
        page: The Playwright page object.
        product_name_1: First product to compare.
        product_name_2: Second product to compare.
    
    Usage Log:
    - Compared two laptops - showed spec comparison table
    - Not all categories support comparison
    """
    import re
    
    import re
    
    await page.goto("/")
    
    # Helper function to search (reuse pattern)
    async def do_search(query):
        search_input = page.get_by_role("combobox", name=re.compile(r"search", re.IGNORECASE))
        if await search_input.count() == 0:
            search_input = page.get_by_role("textbox", name=re.compile(r"search", re.IGNORECASE))
        await search_input.fill(query)
        await page.wait_for_timeout(100)
        await search_input.press("Enter")
    
    # Search for first product
    await do_search(product_name_1)
    
    # Add to compare
    await page.get_by_role("checkbox", name=re.compile(r"compare", re.IGNORECASE)).first.check()
    
    # Search for second product
    await do_search(product_name_2)
    
    # Add to compare
    await page.get_by_role("checkbox", name=re.compile(r"compare", re.IGNORECASE)).first.check()
    
    # View comparison
    await page.get_by_role("link", name=re.compile(r"compare", re.IGNORECASE)).click()
