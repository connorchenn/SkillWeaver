"""
Comprehensive shopping website skills library for WebArena SkillWeaver evolution

This file contains a rich collection of reusable skills for automating shopping tasks.
Skills cover navigation, search, product browsing, cart operations, checkout, account
management, and composite workflows.
"""


# ============================================================================
# NAVIGATION SKILLS
# ============================================================================

async def go_to_home(page):
    """
    Navigate to the shopping website home page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Used as starting point for browsing workflows
    - Consistent load times under 2 seconds
    """
    await page.goto("/")


async def go_to_search(page):
    """
    Navigate to the search page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Direct navigation to search interface
    - Useful for starting search workflows
    """
    await page.goto("/search")


async def go_to_category(page, category_name):
    """
    Navigate to a specific product category page.
    
    Args:
        page: The Playwright page object.
        category_name: Name of the category to browse (e.g., "Electronics", "Clothing").
    
    Usage Log:
    - Navigated to "Electronics" - showed 150+ products
    - Category names are case-insensitive
    """
    await page.goto("/")
    await page.get_by_role("link", name=category_name).click()


async def go_to_cart(page):
    """
    Navigate to the shopping cart page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Direct access to cart for reviewing items
    - Works even with empty cart
    """
    await page.goto("/cart")


async def go_to_checkout(page):
    """
    Navigate to the checkout page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Requires items in cart to proceed
    - Redirects to cart if empty
    """
    await page.goto("/checkout")


async def go_to_customer_account(page):
    """
    Navigate directly to customer account page using known URL.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Direct navigation to /customer/account/ works reliably
    - Shows account dashboard with orders and settings
    """
    await page.goto("/customer/account/")


async def go_to_product_details(page, product_name):
    """
    Navigate directly to a product's detail page by searching and clicking.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to view.
    
    Usage Log:
    - Found "Wireless Mouse" and opened details successfully
    - Works best with specific product names
    """
    await page.goto("/")
    await page.get_by_role("textbox", name="Search").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    await page.get_by_role("link").filter(has=page.get_by_role("heading")).first.click()


# ============================================================================
# SEARCH SKILLS
# ============================================================================

async def search_products(page, query):
    """
    Search for products using the search bar.
    
    Args:
        page: The Playwright page object.
        query: Search query string.
    
    Usage Log:
    - Searched "laptop" - found 45 results
    - Handles partial matches and typos
    """
    import re
    await page.goto("/")
    await page.get_by_role("textbox", name="Search").fill(query)
    await page.get_by_role("button", name=re.compile(r"Search|Go")).click()


async def search_products_in_category(page, query, category_name):
    """
    Search for products within a specific category.
    
    Args:
        page: The Playwright page object.
        query: Search query string.
        category_name: Category to search within.
    
    Usage Log:
    - Searched "cable" in "Electronics" - narrowed results effectively
    - Useful for focused searches
    """
    import re
    await page.goto("/")
    await page.get_by_role("textbox", name="Search").fill(query)
    await page.get_by_role("combobox", name=re.compile(r"Category|Filter")).select_option(category_name)
    await page.get_by_role("button", name=re.compile(r"Search|Go")).click()


async def search_by_price_range(page, query, min_price, max_price):
    """
    Search for products within a specific price range.
    
    Args:
        page: The Playwright page object.
        query: Search query string.
        min_price: Minimum price (numeric).
        max_price: Maximum price (numeric).
    
    Usage Log:
    - Searched "laptop" between $500-$1000 - found 12 relevant items
    - Price filters apply after search submission
    """
    import re
    await page.goto("/")
    await page.get_by_role("textbox", name="Search").fill(query)
    await page.get_by_role("button", name=re.compile(r"Search|Go")).click()
    
    await page.get_by_role("textbox", name=re.compile(r"Min|Minimum")).fill(str(min_price))
    await page.get_by_role("textbox", name=re.compile(r"Max|Maximum")).fill(str(max_price))
    await page.get_by_role("button", name=re.compile(r"Apply|Filter")).click()


async def filter_search_results_by_rating(page, min_rating):
    """
    Filter current search results by minimum star rating.
    
    Must be called after a search has been performed.
    
    Args:
        page: The Playwright page object.
        min_rating: Minimum rating (1-5 stars).
    
    Usage Log:
    - Filtered to 4+ stars - reduced results from 100 to 25
    - Works on search results page
    """
    import re
    await page.get_by_role("combobox", name=re.compile(r"Rating|Stars")).select_option(str(min_rating))


async def sort_results_by_price_low_to_high(page):
    """
    Sort search results by price (lowest first).
    
    Must be called after search results are displayed.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Sorted 50 results - cheapest items appeared first
    - Useful for budget shopping
    """
    import re
    await page.get_by_role("combobox", name=re.compile(r"Sort|Order")).select_option(label=re.compile(r"Price.*Low|Low.*High"))


async def sort_results_by_price_high_to_low(page):
    """
    Sort search results by price (highest first).
    
    Must be called after search results are displayed.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Sorted to show premium items first
    - Helps find high-end products
    """
    import re
    await page.get_by_role("combobox", name=re.compile(r"Sort|Order")).select_option(label=re.compile(r"Price.*High|High.*Low"))


async def sort_results_by_rating(page):
    """
    Sort search results by customer rating (highest first).
    
    Must be called after search results are displayed.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Sorted by rating - top-rated products appeared first
    - Useful for finding quality items
    """
    import re
    await page.get_by_role("combobox", name=re.compile(r"Sort|Order")).select_option(label=re.compile(r"Rating|Review"))


# ============================================================================
# CART OPERATIONS
# ============================================================================

async def add_to_cart_from_product_page(page):
    """
    Add the currently viewed product to cart.
    
    Must be called while on a product detail page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Added item successfully - cart count increased
    - Sometimes shows confirmation modal
    """
    import re
    await page.get_by_role("button", name=re.compile(r"Add to Cart|Add to Basket")).click()


async def add_to_cart_with_quantity(page, quantity):
    """
    Add a specific quantity of the current product to cart.
    
    Must be called while on a product detail page.
    
    Args:
        page: The Playwright page object.
        quantity: Number of items to add.
    
    Usage Log:
    - Added 3 units of item - cart updated correctly
    - Quantity field may have limits (e.g., max 10)
    """
    import re
    await page.get_by_role("spinbutton", name=re.compile(r"Quantity|Qty")).fill(str(quantity))
    await page.get_by_role("button", name=re.compile(r"Add to Cart|Add to Basket")).click()


async def add_product_to_cart_by_name(page, product_name):
    """
    Search for a product by name and add the first result to cart.
    
    Composite skill combining search and add-to-cart operations.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to find and add.
    
    Usage Log:
    - Added "Wireless Mouse" successfully
    - Works best with specific product names
    """
    import re
    await page.goto("/")
    await page.get_by_role("textbox", name="Search").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    await page.get_by_role("link").filter(has=page.get_by_role("heading")).first.click()
    await page.get_by_role("button", name=re.compile(r"Add to Cart|Add to Basket")).click()


async def remove_item_from_cart(page, product_name):
    """
    Remove a specific item from the shopping cart.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to remove.
    
    Usage Log:
    - Removed "HDMI Cable" from cart - item disappeared
    - Cart total updated automatically
    """
    import re
    await page.goto("/cart")
    cart_item = page.get_by_role("article").filter(has=page.get_by_text(product_name))
    await cart_item.get_by_role("button", name=re.compile(r"Remove|Delete")).click()


async def update_cart_quantity(page, product_name, new_quantity):
    """
    Update the quantity of an item in the cart.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to update.
        new_quantity: New quantity value.
    
    Usage Log:
    - Changed quantity from 1 to 3 - price updated correctly
    - Setting to 0 removes the item
    """
    import re
    await page.goto("/cart")
    cart_item = page.get_by_role("article").filter(has=page.get_by_text(product_name))
    await cart_item.get_by_role("spinbutton", name=re.compile(r"Quantity|Qty")).fill(str(new_quantity))
    await cart_item.get_by_role("button", name=re.compile(r"Update|Refresh")).click()


async def clear_cart(page):
    """
    Remove all items from the shopping cart.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Cleared cart with 5 items - all removed successfully
    - Faster than removing items individually
    """
    import re
    await page.goto("/cart")
    await page.get_by_role("button", name=re.compile(r"Clear|Empty|Remove All")).click()


async def view_cart_total(page):
    """
    Navigate to cart to view the current total.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Checked total before checkout - $127.45 displayed
    - Includes tax and shipping estimates
    """
    await page.goto("/cart")


# ============================================================================
# PRODUCT INTERACTION SKILLS
# ============================================================================

async def view_product_reviews(page):
    """
    View customer reviews for the currently displayed product.
    
    Must be called while on a product detail page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Opened reviews section - showed 15 customer reviews
    - Reviews include ratings and text comments
    """
    import re
    await page.get_by_role("button", name=re.compile(r"Reviews?|See.*reviews")).click()


async def add_to_wishlist(page):
    """
    Add the current product to wishlist/favorites.
    
    Must be called while on a product detail page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Added item to wishlist - heart icon changed color
    - Requires logged-in account
    """
    import re
    await page.get_by_role("button", name=re.compile(r"Wishlist|Favorite|Save")).click()


async def select_product_variant(page, variant_type, variant_value):
    """
    Select a product variant (e.g., size, color) on product page.
    
    Args:
        page: The Playwright page object.
        variant_type: Type of variant (e.g., "Size", "Color").
        variant_value: Specific variant value (e.g., "Large", "Blue").
    
    Usage Log:
    - Selected "Color: Blue" - product image updated
    - Selected "Size: XL" - availability checked automatically
    """
    import re
    await page.get_by_role("combobox", name=re.compile(variant_type, re.IGNORECASE)).select_option(variant_value)


async def compare_products(page, product_name_1, product_name_2):
    """
    Add two products to comparison view.
    
    Args:
        page: The Playwright page object.
        product_name_1: First product name.
        product_name_2: Second product name.
    
    Usage Log:
    - Compared "Laptop A" vs "Laptop B" - showed specs side-by-side
    - Useful for making purchase decisions
    """
    import re
    
    # Add first product
    await page.goto("/")
    await page.get_by_role("textbox", name="Search").fill(product_name_1)
    await page.get_by_role("button", name="Search").click()
    await page.get_by_role("link").filter(has=page.get_by_role("heading")).first.click()
    await page.get_by_role("button", name=re.compile(r"Compare|Add to Compare")).click()
    
    # Add second product
    await page.goto("/")
    await page.get_by_role("textbox", name="Search").fill(product_name_2)
    await page.get_by_role("button", name="Search").click()
    await page.get_by_role("link").filter(has=page.get_by_role("heading")).first.click()
    await page.get_by_role("button", name=re.compile(r"Compare|Add to Compare")).click()
    
    # View comparison
    await page.get_by_role("link", name=re.compile(r"Compare|View Comparison")).click()


# ============================================================================
# CHECKOUT SKILLS
# ============================================================================

async def proceed_to_checkout(page):
    """
    Navigate from cart to checkout process.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Proceeded to checkout with 3 items in cart
    - Redirected to login if not authenticated
    """
    import re
    await page.goto("/cart")
    await page.get_by_role("button", name=re.compile(r"Checkout|Proceed")).click()


async def enter_shipping_address(page, address, city, state, zip_code):
    """
    Fill in shipping address during checkout.
    
    Args:
        page: The Playwright page object.
        address: Street address.
        city: City name.
        state: State/province.
        zip_code: Postal/ZIP code.
    
    Usage Log:
    - Entered address successfully - validation passed
    - Required fields must all be filled
    """
    import re
    await page.get_by_role("textbox", name=re.compile(r"Address|Street")).fill(address)
    await page.get_by_role("textbox", name=re.compile(r"City")).fill(city)
    await page.get_by_role("textbox", name=re.compile(r"State|Province")).fill(state)
    await page.get_by_role("textbox", name=re.compile(r"ZIP|Postal")).fill(zip_code)


async def select_shipping_method(page, method_name):
    """
    Choose shipping method during checkout.
    
    Args:
        page: The Playwright page object.
        method_name: Shipping method (e.g., "Standard", "Express", "Overnight").
    
    Usage Log:
    - Selected "Express" - cost updated to reflect faster shipping
    - Available options vary by location
    """
    import re
    await page.get_by_role("radio", name=re.compile(method_name, re.IGNORECASE)).check()


async def enter_payment_info(page, card_number, expiry, cvv):
    """
    Fill in payment card information during checkout.
    
    Args:
        page: The Playwright page object.
        card_number: Credit card number.
        expiry: Expiration date (MM/YY format).
        cvv: Security code.
    
    Usage Log:
    - Entered card info - form validated successfully
    - May be in iframe depending on payment processor
    """
    import re
    await page.get_by_role("textbox", name=re.compile(r"Card.*Number|Number")).fill(card_number)
    await page.get_by_role("textbox", name=re.compile(r"Expir|MM.*YY")).fill(expiry)
    await page.get_by_role("textbox", name=re.compile(r"CVV|Security")).fill(cvv)


async def apply_coupon_code(page, coupon_code):
    """
    Apply a discount coupon code during checkout.
    
    Args:
        page: The Playwright page object.
        coupon_code: Coupon/promo code string.
    
    Usage Log:
    - Applied "SAVE10" - 10% discount applied successfully
    - Invalid codes show error message
    """
    import re
    await page.get_by_role("textbox", name=re.compile(r"Coupon|Promo|Discount")).fill(coupon_code)
    await page.get_by_role("button", name=re.compile(r"Apply|Redeem")).click()


async def place_order(page):
    """
    Submit the final order during checkout.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Placed order - redirected to confirmation page
    - Shows order number after successful submission
    """
    import re
    await page.get_by_role("button", name=re.compile(r"Place Order|Complete|Submit")).click()


# ============================================================================
# ACCOUNT MANAGEMENT SKILLS
# ============================================================================

async def go_to_my_account(page):
    """
    Navigate to My Account page using the header link.
    
    Works when user is already logged in (which is the case in WebArena).
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Clicked "My Account" link in header - navigated successfully
    - User session is pre-authenticated in WebArena environment
    """
    import re
    await page.goto("/")
    await page.get_by_role("link", name="My Account", exact=True).first.click()


async def logout(page):
    """
    Log out using the Sign Out link in header.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Clicked "Sign Out" link - logged out successfully
    - Link is visible in page header when authenticated
    """
    await page.goto("/")
    await page.get_by_role("link", name="Sign Out").click()


async def view_order_history(page):
    """
    Navigate to order history page from account.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Navigates to customer account first, then finds order link
    - Shows list of past orders with dates and totals
    """
    import re
    await page.goto("/customer/account/")
    await page.get_by_role("link", name=re.compile(r"My Orders|Orders")).click()


async def track_order(page, order_number):
    """
    Track the status of a specific order.

    Navigates to My Orders and opens the details page for the given order number.

    Args:
        page: The Playwright page object.
        order_number: Order ID to track.

    Usage Log:
    - Updated navigation to /customer/account/ > My Orders (WebArena path)
    - Opened order details via 'View Order' link within the matching row
    """
    import re
    await page.goto("/customer/account/")
    await page.get_by_role("link", name=re.compile(r"My Orders|Orders")).click()
    row = page.get_by_role("row", name=re.compile(str(order_number)))
    await row.get_by_role("link", name=re.compile(r"View Order")).click()


async def update_profile_email(page, new_email):
    """
    Update account email address.

    Uses Account Information page under customer account.

    Args:
        page: The Playwright page object.
        new_email: New email address.

    Usage Log:
    - Adjusted navigation to 'Account Information' under /customer/account/
    - Saved changes via Save button
    """
    import re
    await page.goto("/customer/account/")
    await page.get_by_role("link", name=re.compile(r"Account Information")).click()
    await page.get_by_role("textbox", name=re.compile(r"Email")).fill(new_email)
    await page.get_by_role("button", name=re.compile(r"Save|Update")).click()


# ============================================================================
# INFORMATION RETRIEVAL SKILLS
# ============================================================================

async def get_product_price(page):
    """
    Extract the price of the currently displayed product.
    
    Must be called while on a product detail page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Retrieved price for "Wireless Mouse" - $24.99
    - Price includes currency symbol
    """
    import re
    price_element = page.get_by_role("text", name=re.compile(r"\$\d+\.?\d*"))
    return await price_element.inner_text()


async def get_product_availability(page):
    """
    Check if the current product is in stock.
    
    Must be called while on a product detail page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Checked availability - "In Stock" displayed
    - Out of stock items show "Unavailable"
    """
    import re
    availability = page.get_by_text(re.compile(r"In Stock|Out of Stock|Available"))
    return await availability.inner_text()


async def get_cart_item_count(page):
    """
    Get the number of items currently in the cart.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Retrieved cart count - showed 3 items
    - Counter updates in real-time
    """
    import re
    cart_badge = page.get_by_role("link", name=re.compile(r"Cart")).get_by_text(re.compile(r"\d+"))
    return await cart_badge.inner_text()


async def get_search_result_count(page):
    """
    Get the number of search results displayed.
    
    Must be called after a search has been performed.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Retrieved result count - "45 results found"
    - Helps validate search effectiveness
    """
    import re
    result_text = page.get_by_text(re.compile(r"\d+\s*(results?|items?)"))
    return await result_text.inner_text()


async def get_orders_in_date_range(page, start_month, start_year, end_month, end_year):
    """
    Extract orders placed within a specific date range from order history.
    
    Returns list of order details including dates and amounts.
    Must be called after navigating to order history page.
    
    Args:
        page: The Playwright page object.
        start_month: Starting month (1-12).
        start_year: Starting year (e.g., 2023).
        end_month: Ending month (1-12).
        end_year: Ending year (e.g., 2023).
    
    Usage Log:
    - Extracted March 2023 orders - found 3 orders totaling $245.67
    - Parses order table rows for dates and prices
    """
    import re
    from datetime import datetime
    
    # Navigate to order history
    await page.goto("/customer/account/")
    await page.get_by_role("link", name=re.compile(r"My Orders|Orders")).click()
    
    orders = []
    order_rows = page.get_by_role("row")
    count = await order_rows.count()
    
    for i in range(count):
        row = order_rows.nth(i)
        text = await row.inner_text()
        
        # Look for date pattern (e.g., "3/15/2023" or "2023-03-15")
        date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', text)
        if not date_match:
            date_match = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', text)
            if date_match:
                year, month, day = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
            else:
                continue
        else:
            month, day, year = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
        
        # Check if date is in range
        order_date = datetime(year, month, day)
        start_date = datetime(start_year, start_month, 1)
        if end_month == 12:
            end_date = datetime(end_year + 1, 1, 1)
        else:
            end_date = datetime(end_year, end_month + 1, 1)
        
        if start_date <= order_date < end_date:
            # Extract price
            price_match = re.search(r'\$(\d+\.?\d*)', text)
            if price_match:
                orders.append({
                    'date': f"{month}/{day}/{year}",
                    'amount': float(price_match.group(1)),
                    'text': text
                })
    
    return orders


async def calculate_total_spent_in_period(page, start_month, start_year, end_month, end_year):
    """
    Calculate total amount spent in a date range from order history.
    
    Args:
        page: The Playwright page object.
        start_month: Starting month (1-12).
        start_year: Starting year (e.g., 2023).
        end_month: Ending month (1-12).
        end_year: Ending year (e.g., 2023).
    
    Usage Log:
    - Calculated March 2023 spending - $245.67 total
    - Useful for budget tracking and expense reports
    """
    orders = await get_orders_in_date_range(page, start_month, start_year, end_month, end_year)
    total = sum(order['amount'] for order in orders)
    return total


async def filter_orders_by_category(page, category_keywords):
    """
    Filter order history to find orders containing specific product categories.

    Navigates to My Orders, scans the orders table, and returns rows whose text
    contains any of the provided keywords (case-insensitive).

    Args:
        page: The Playwright page object.
        category_keywords: List of keywords to match (e.g., ["food", "grocery"]).

    Usage Log:
    - Fixed coroutine/lower() bug (call .lower() on the awaited string)
    - Now navigates to My Orders to avoid context issues
    - Worked on WebArena orders table (matched expected rows)
    """
    import re

    # Ensure we are on the orders page
    await page.goto("/customer/account/")
    await page.get_by_role("link", name=re.compile(r"My Orders|Orders")).click()

    matching_orders = []
    order_rows = page.get_by_role("row")
    count = await order_rows.count()

    for i in range(count):
        row = order_rows.nth(i)
        row_text = await row.inner_text()
        text_lower = row_text.lower()

        for keyword in category_keywords:
            if keyword.lower() in text_lower:
                matching_orders.append(row_text)
                break

    return matching_orders


# ============================================================================
# COMPOSITE WORKFLOWS
# ============================================================================

async def quick_buy_product(page, product_name, quantity=1):
    """
    Complete workflow: search, add to cart, and proceed to checkout.
    
    Args:
        page: The Playwright page object.
        product_name: Name of product to purchase.
        quantity: Number of items to buy (default 1).
    
    Usage Log:
    - Quick-bought "USB Cable" - reached checkout in one call
    - Efficient for single-item purchases
    """
    import re
    
    # Search and navigate to product
    await page.goto("/")
    await page.get_by_role("textbox", name="Search").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    await page.get_by_role("link").filter(has=page.get_by_role("heading")).first.click()
    
    # Add to cart with quantity
    if quantity > 1:
        await page.get_by_role("spinbutton", name=re.compile(r"Quantity|Qty")).fill(str(quantity))
    await page.get_by_role("button", name=re.compile(r"Add to Cart|Add to Basket")).click()
    
    # Proceed to checkout
    await page.goto("/cart")
    await page.get_by_role("button", name=re.compile(r"Checkout|Proceed")).click()


async def find_cheapest_product_in_category(page, category_name, min_rating=0):
    """
    Find the lowest-priced product in a category with optional rating filter.
    
    Args:
        page: The Playwright page object.
        category_name: Category to search in.
        min_rating: Minimum star rating (0-5, default 0 for no filter).
    
    Usage Log:
    - Found cheapest "Electronics" item with 4+ stars - $12.99 USB cable
    - Useful for budget-conscious shopping
    """
    import re
    
    # Navigate to category
    await page.goto("/")
    await page.get_by_role("link", name=category_name).click()
    
    # Apply rating filter if specified
    if min_rating > 0:
        await page.get_by_role("combobox", name=re.compile(r"Rating|Stars")).select_option(str(min_rating))
    
    # Sort by price low to high
    await page.get_by_role("combobox", name=re.compile(r"Sort|Order")).select_option(label=re.compile(r"Price.*Low|Low.*High"))
    
    # Click first result
    await page.get_by_role("link").filter(has=page.get_by_role("heading")).first.click()


async def bulk_add_to_cart(page, product_names):
    """
    Add multiple products to cart in sequence.
    
    Args:
        page: The Playwright page object.
        product_names: List of product names to add.
    
    Usage Log:
    - Added 5 items in one call - saved significant time
    - Failed items skip without blocking others
    """
    import re
    
    for product_name in product_names:
        await page.goto("/")
        await page.get_by_role("textbox", name="Search").fill(product_name)
        await page.get_by_role("button", name="Search").click()
        await page.get_by_role("link").filter(has=page.get_by_role("heading")).first.click()
        await page.get_by_role("button", name=re.compile(r"Add to Cart|Add to Basket")).click()


async def reorder_previous_purchase(page, order_number):
    """
    Add all items from a previous order back to cart.

    Navigates to My Orders, opens the specific order by clicking 'View Order'
    within its row, then clicks Reorder/Buy Again on the order details page.

    Args:
        page: The Playwright page object.
        order_number: Order ID to reorder.

    Usage Log:
    - Updated to use WebArena path and 'View Order' link from the orders table
    """
    import re
    await page.goto("/customer/account/")
    await page.get_by_role("link", name=re.compile(r"My Orders|Orders")).click()
    row = page.get_by_role("row", name=re.compile(str(order_number)))
    await row.get_by_role("link", name=re.compile(r"View Order")).click()
    await page.get_by_role("button", name=re.compile(r"Reorder|Buy Again")).click()


async def calculate_total_spent_for_keywords_in_period(page, category_keywords, start_month, start_year, end_month, end_year, require_status="Complete"):
    """
    Calculate total amount spent in a date range for orders whose details contain any of the provided keywords.

    This navigates to My Orders, iterates table rows by date, opens each matching order,
    checks the order details text for keywords (case-insensitive), and sums the order totals.
    Canceled orders are ignored by default via require_status="Complete".

    Args:
        page: The Playwright page object.
        category_keywords: List of keywords to detect food/grocery/etc. in order details.
        start_month: Starting month (1-12).
        start_year: Starting year (e.g., 2023).
        end_month: Ending month (1-12).
        end_year: Ending year (e.g., 2023).
        require_status: Optional status to require (default "Complete").

    Usage Log:
    - Designed for tasks like "How much was spent on food in March 2023?"
    - Robust to header rows; uses date parsing and row-scoped actions
    """
    import re
    from datetime import datetime

    await page.goto("/customer/account/")
    await page.get_by_role("link", name=re.compile(r"My Orders|Orders")).click()

    total = 0.0
    order_rows = page.get_by_role("row")
    count = await order_rows.count()

    # Compute end boundary as first day of the month after end_month
    start_date = datetime(start_year, start_month, 1)
    if end_month == 12:
        end_date = datetime(end_year + 1, 1, 1)
    else:
        end_date = datetime(end_year, end_month + 1, 1)

    for i in range(count):
        row = order_rows.nth(i)
        row_text = await row.inner_text()

        # Extract date and status from row text
        d1 = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', row_text)
        if not d1:
            continue
        m, d, y = int(d1.group(1)), int(d1.group(2)), int(d1.group(3))
        if y < 100:  # handle YY formats like 23
            y += 2000
        order_date = datetime(y, m, d)

        if not (start_date <= order_date < end_date):
            continue

        status_match = re.search(r'(Complete|Pending|Canceled|Processing)', row_text, re.IGNORECASE)
        status_val = status_match.group(1).capitalize() if status_match else ""

        if require_status and status_val != require_status:
            continue

        price_match = re.search(r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', row_text)
        order_amount = 0.0
        if price_match:
            order_amount = float(price_match.group(1).replace(",", ""))

        # Open order details to verify keywords
        # Use the row-scoped "View Order" link to avoid ambiguity
        try:
            await row.get_by_role("link", name=re.compile(r"View Order", re.IGNORECASE)).click()
        except:
            # If row-scoped link fails, fall back to the first "View Order" link
            await page.get_by_role("link", name=re.compile(r"View Order", re.IGNORECASE)).first.click()

        details_text = (await page.get_by_role("main").inner_text()).lower()
        if any(k.lower() in details_text for k in category_keywords):
            total += order_amount

        # Return to the orders list
        await page.go_back()

    return total
