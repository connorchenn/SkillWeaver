"""
Shopping Admin Skills Library for WebArena SkillWeaver

Comprehensive skill set for automating shopping admin website tasks.
Covers products, orders, customers, categories, and common admin workflows.
"""


# ============================================================================
# NAVIGATION SKILLS - Basic navigation to key admin sections
# ============================================================================

async def navigate_to_dashboard(page):
    """
    Navigate to the admin dashboard homepage.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Used as starting point for many workflows
    """
    await page.goto("/admin")


async def navigate_to_catalog_products(page):
    """
    Navigate to the catalog products listing page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Primary entry point for product management tasks
    """
    await page.goto("/admin/catalog/product")


async def navigate_to_categories(page):
    """
    Navigate to the categories management page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Used for category creation and organization
    """
    await page.goto("/admin/catalog/category")


async def navigate_to_orders(page):
    """
    Navigate to the orders management page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Entry point for order processing workflows
    """
    await page.goto("/admin/sales/order")


async def navigate_to_customers(page):
    """
    Navigate to the customers management page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Used for customer account management
    """
    await page.goto("/admin/customer")


async def navigate_to_create_product(page):
    """
    Navigate directly to the create new product page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Shortcut for product creation workflows
    """
    await page.goto("/admin/catalog/product/new")


async def navigate_to_reports(page):
    """
    Navigate to the reports section.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Access point for sales and product reports
    """
    await page.goto("/admin/reports")


async def navigate_to_sales_reports(page):
    """
    Navigate to sales reports section.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - For viewing sales analytics and order statistics
    """
    await page.goto("/admin/reports/sales")


async def navigate_to_marketing(page):
    """
    Navigate to marketing section.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Access promotions, coupons, and marketing campaigns
    """
    await page.goto("/admin/marketing")


async def navigate_to_stores(page):
    """
    Navigate to stores configuration.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Manage store settings and configurations
    """
    await page.goto("/admin/stores")


async def navigate_to_system(page):
    """
    Navigate to system configuration.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Access system settings and configuration
    """
    await page.goto("/admin/system")


# ============================================================================
# SEARCH & FILTER SKILLS - Finding specific items
# ============================================================================

async def search_products_by_name(page, product_name):
    """
    Search for products by name in the catalog.
    
    Navigates to products page and uses the search/filter functionality
    to find products matching the given name.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to search for.
    
    Usage Log:
    - Used in Task 1 to find "Sprite Stasis Ball 65 cm" - successfully found product
    - Search is case-insensitive and matches substrings
    """
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()


async def get_product_attribute_set(page, product_name):
    """
    Get the attribute set (brand) of a product by searching for it.
    
    Searches for the product and returns its attribute set which often represents the brand.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to look up.
    
    Usage Log:
    - Created for Task 1 to extract brand from "Sprite Stasis Ball 65 cm" - returns "Sprite Stasis Ball"
    - Works even if columns are reordered by locating the "Attribute Set" header dynamically
    - Fallback to 6th column when header detection is unavailable
    """
    import re
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    # Scope to the products grid
    table = page.get_by_role("table").filter(
        has=page.get_by_role("columnheader", name=re.compile(r"Attribute Set|Name", re.I))
    ).first
    
    # Determine index of "Attribute Set" column
    headers = await table.get_by_role("columnheader").all_text_contents()
    attr_idx = None
    for i, h in enumerate(headers):
        if h and re.search(r"attribute\s*set", h, re.I):
            attr_idx = i
            break
    if attr_idx is None:
        attr_idx = 5  # Fallback commonly observed position
    
    # Read the attribute set value from the row containing the product name
    row = table.get_by_role("row").filter(has=page.get_by_text(product_name)).first
    cell = row.get_by_role("cell").nth(attr_idx)
    text = await cell.text_content()
    return (text or "").strip()


async def open_product_edit_page(page, product_name):
    """
    Search for a product and open its edit page.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product to edit.
    
    Usage Log:
    - Reusable pattern for accessing product details
    """
    import re
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    await page.get_by_role("link", name=product_name).first.click()


async def search_products_by_sku(page, sku):
    """
    Search for products by SKU in the catalog.
    
    Args:
        page: The Playwright page object.
        sku: SKU code to search for.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="SKU").fill(sku)
    await page.get_by_role("button", name="Search").click()


async def filter_products_by_status(page, status):
    """
    Filter products by enabled/disabled status.
    
    Args:
        page: The Playwright page object.
        status: Status to filter by (e.g., "Enabled", "Disabled").
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto("/admin/catalog/product")
    await page.get_by_role("combobox", name="Status").select_option(status)
    await page.get_by_role("button", name="Search").click()


async def search_orders_by_id(page, order_id):
    """
    Search for a specific order by its ID.
    
    Args:
        page: The Playwright page object.
        order_id: Order ID to search for.
    
    Usage Log:
    - Basic order lookup by ID
    """
    await page.goto("/admin/sales/order")
    await page.get_by_role("textbox", name="ID").fill(str(order_id))
    await page.get_by_role("button", name="Search").click()


async def open_order_filters(page):
    """
    Open the advanced filters panel on the orders page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Used in Task 111 to access date range filters
    - Filters button has icon "\ue605Filters"
    """
    await page.goto("/admin/sales/order")
    import re
    await page.get_by_role("button", name=re.compile(r"Filters")).click()


async def filter_orders_by_date_range(page, from_date, to_date):
    """
    Filter orders by purchase date range.
    
    Opens filters and sets date range for order search.
    
    Args:
        page: The Playwright page object.
        from_date: Start date in format like "02/01/2022"
        to_date: End date in format like "11/30/2022"
    
    Usage Log:
    - Created for Task 111 to filter Feb-Nov 2022 orders
    - Date format appears to be MM/DD/YYYY
    """
    import re
    await page.goto("/admin/sales/order")
    await page.get_by_role("button", name=re.compile(r"Filters")).click()
    
    # Fill in date range in the Purchase Date group
    date_group = page.get_by_role("group", name="Purchase Date")
    await date_group.get_by_role("textbox", name="from").fill(from_date)
    await date_group.get_by_role("textbox", name="to").fill(to_date)
    
    await page.get_by_role("button", name="Apply Filters").click()


async def filter_orders_by_status(page, status):
    """
    Filter orders by their status.
    
    Args:
        page: The Playwright page object.
        status: Order status (e.g., "Complete", "Processing", "Pending", "Canceled")
    
    Usage Log:
    - Created to filter for successful/complete orders
    - Status combobox has many options including "Complete"
    """
    import re
    await page.goto("/admin/sales/order")
    await page.get_by_role("button", name=re.compile(r"Filters")).click()
    
    # Select status from combobox - there may be multiple, need to find the right one
    await page.get_by_role("combobox").filter(has=page.get_by_text("Complete")).select_option(status)
    
    await page.get_by_role("button", name="Apply Filters").click()


async def filter_orders_by_date_and_status(page, from_date, to_date, status):
    """
    Filter orders by both date range and status.
    
    Composite skill for filtering orders with multiple criteria.
    
    Args:
        page: The Playwright page object.
        from_date: Start date in format like "02/01/2022"
        to_date: End date in format like "11/30/2022"
        status: Order status (e.g., "Complete", "Processing")
    
    Usage Log:
    - Created for Task 111 to find complete orders in date range
    """
    import re
    await page.goto("/admin/sales/order")
    await page.get_by_role("button", name=re.compile(r"Filters")).click()
    
    # Set date range
    date_group = page.get_by_role("group", name="Purchase Date")
    await date_group.get_by_role("textbox", name="from").fill(from_date)
    await date_group.get_by_role("textbox", name="to").fill(to_date)
    
    # Set status
    await page.get_by_role("combobox").filter(has=page.get_by_text(status)).select_option(status)
    
    await page.get_by_role("button", name="Apply Filters").click()


async def search_customers_by_email(page, email):
    """
    Search for customers by email address.
    
    Args:
        page: The Playwright page object.
        email: Email address to search for.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto("/admin/customer")
    await page.get_by_role("textbox", name="Email").fill(email)
    await page.get_by_role("button", name="Search").click()


async def search_customers_by_name(page, name):
    """
    Search for customers by name.
    
    Args:
        page: The Playwright page object.
        name: Customer name to search for.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto("/admin/customer")
    await page.get_by_role("textbox", name="Name").fill(name)
    await page.get_by_role("button", name="Search").click()


async def search_products_by_price_range(page, min_price, max_price):
    """
    Search for products within a price range.
    
    Args:
        page: The Playwright page object.
        min_price: Minimum price value.
        max_price: Maximum price value.
    
    Usage Log:
    - Useful for finding products in specific price brackets
    """
    import re
    await page.goto("/admin/catalog/product")
    await page.get_by_role("button", name=re.compile(r"Filters")).click()
    
    price_group = page.get_by_role("group", name="Price")
    await price_group.get_by_role("textbox", name="from").fill(str(min_price))
    await price_group.get_by_role("textbox", name="to").fill(str(max_price))
    
    await page.get_by_role("button", name="Apply Filters").click()


async def search_products_by_quantity_range(page, min_qty, max_qty):
    """
    Search for products by quantity/stock level.
    
    Args:
        page: The Playwright page object.
        min_qty: Minimum quantity.
        max_qty: Maximum quantity.
    
    Usage Log:
    - Find low-stock or overstocked items
    """
    import re
    await page.goto("/admin/catalog/product")
    await page.get_by_role("button", name=re.compile(r"Filters")).click()
    
    qty_group = page.get_by_role("group", name="Quantity")
    await qty_group.get_by_role("textbox", name="from").fill(str(min_qty))
    await qty_group.get_by_role("textbox", name="to").fill(str(max_qty))
    
    await page.get_by_role("button", name="Apply Filters").click()


async def clear_product_filters(page):
    """
    Clear all active filters on the products page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Reset search/filter state
    """
    await page.goto("/admin/catalog/product")
    await page.get_by_role("button", name="Clear all").click()


async def clear_order_filters(page):
    """
    Clear all active filters on the orders page.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Reset order search/filter state by clicking the dedicated "Clear all" control
    - More reliable than toggling the filter panel and pressing Cancel
    """
    import re
    await page.goto("/admin/sales/order")
    await page.get_by_role("button", name=re.compile(r"Clear all", re.I)).click()


# ============================================================================
# PRODUCT MANAGEMENT SKILLS - Creating and editing products
# ============================================================================

async def create_simple_product(page, product_name, sku, price, quantity):
    """
    Create a new simple product with basic information.
    
    Navigates to product creation page and fills in essential fields.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product.
        sku: SKU code for the product.
        price: Product price.
        quantity: Initial stock quantity.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto("/admin/catalog/product/new")
    
    await page.get_by_role("textbox", name="Product Name").fill(product_name)
    await page.get_by_role("textbox", name="SKU").fill(sku)
    await page.get_by_role("textbox", name="Price").fill(str(price))
    await page.get_by_role("textbox", name="Quantity").fill(str(quantity))
    
    await page.get_by_role("button", name="Save").click()


async def update_product_price(page, product_name, new_price):
    """
    Search for a product and update its price.
    
    Composite skill combining search and price update.
    
    Args:
        page: The Playwright page object.
        product_name: Name of product to update.
        new_price: New price value.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    # Click the first result to edit
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("textbox", name="Price").fill(str(new_price))
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def update_product_quantity(page, product_name, new_quantity):
    """
    Search for a product and update its stock quantity.
    
    Args:
        page: The Playwright page object.
        product_name: Name of product to update.
        new_quantity: New quantity value.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("textbox", name="Quantity").fill(str(new_quantity))
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def disable_product(page, product_name):
    """
    Search for a product and disable it.
    
    Args:
        page: The Playwright page object.
        product_name: Name of product to disable.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("combobox", name="Enable Product").select_option("No")
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def enable_product(page, product_name):
    """
    Search for a product and enable it.
    
    Args:
        page: The Playwright page object.
        product_name: Name of product to enable.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("combobox", name="Enable Product").select_option("Yes")
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def delete_product(page, product_name):
    """
    Search for a product and delete it.
    
    Args:
        page: The Playwright page object.
        product_name: Name of product to delete.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("button", name=re.compile(r"Delete")).click()
    # Confirm deletion if prompted
    await page.get_by_role("button", name=re.compile(r"OK|Confirm")).click()


# ============================================================================
# CATEGORY MANAGEMENT SKILLS
# ============================================================================

async def create_category(page, category_name):
    """
    Create a new product category.
    
    Args:
        page: The Playwright page object.
        category_name: Name for the new category.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto("/admin/catalog/category")
    await page.get_by_role("button", name="Add Category").click()
    await page.get_by_role("textbox", name="Name").fill(category_name)
    await page.get_by_role("button", name="Save").click()


async def assign_product_to_category(page, product_name, category_name):
    """
    Assign a product to a specific category.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product.
        category_name: Name of the category to assign to.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    # Look for category selection - might be in different sections
    await page.get_by_role("combobox", name=re.compile(r"Category|Categories")).select_option(category_name)
    await page.get_by_role("button", name=re.compile(r"Save")).click()


# ============================================================================
# ORDER MANAGEMENT SKILLS
# ============================================================================

async def view_order_details(page, order_id):
    """
    Navigate to view details of a specific order.
    
    Args:
        page: The Playwright page object.
        order_id: ID of the order to view.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto(f"/admin/sales/order/view/order_id/{order_id}")


async def change_order_status(page, order_id, new_status):
    """
    Change the status of an order.
    
    Args:
        page: The Playwright page object.
        order_id: ID of the order.
        new_status: New status to set (e.g., "Processing", "Complete", "Canceled").
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto(f"/admin/sales/order/view/order_id/{order_id}")
    
    await page.get_by_role("combobox", name="Status").select_option(new_status)
    await page.get_by_role("button", name=re.compile(r"Submit|Save")).click()


async def create_invoice_for_order(page, order_id):
    """
    Create an invoice for an order.
    
    Args:
        page: The Playwright page object.
        order_id: ID of the order to invoice.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto(f"/admin/sales/order/view/order_id/{order_id}")
    await page.get_by_role("button", name="Invoice").click()
    await page.get_by_role("button", name="Submit Invoice").click()


async def create_shipment_for_order(page, order_id):
    """
    Create a shipment for an order.
    
    Args:
        page: The Playwright page object.
        order_id: ID of the order to ship.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto(f"/admin/sales/order/view/order_id/{order_id}")
    await page.get_by_role("button", name="Ship").click()
    await page.get_by_role("button", name="Submit Shipment").click()


# ============================================================================
# CUSTOMER MANAGEMENT SKILLS
# ============================================================================

async def create_customer(page, first_name, last_name, email):
    """
    Create a new customer account.
    
    Args:
        page: The Playwright page object.
        first_name: Customer's first name.
        last_name: Customer's last name.
        email: Customer's email address.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto("/admin/customer/new")
    
    await page.get_by_role("textbox", name="First Name").fill(first_name)
    await page.get_by_role("textbox", name="Last Name").fill(last_name)
    await page.get_by_role("textbox", name="Email").fill(email)
    
    await page.get_by_role("button", name="Save Customer").click()


async def view_customer_details(page, email):
    """
    View details of a customer by searching for their email.
    
    Args:
        page: The Playwright page object.
        email: Customer's email address.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    await page.goto("/admin/customer")
    await page.get_by_role("textbox", name="Email").fill(email)
    await page.get_by_role("button", name="Search").click()
    await page.get_by_role("link", name=email).first.click()


async def search_orders_by_customer_name(page, customer_name):
    """
    Search for orders by customer name.
    
    Args:
        page: The Playwright page object.
        customer_name: Name of the customer (Bill-to Name).
    
    Usage Log:
    - Find all orders for a specific customer
    """
    import re
    await page.goto("/admin/sales/order")
    await page.get_by_role("button", name=re.compile(r"Filters")).click()
    await page.get_by_role("textbox", name="Bill-to Name").fill(customer_name)
    await page.get_by_role("button", name="Apply Filters").click()


async def search_orders_by_grand_total_range(page, min_total, max_total):
    """
    Search for orders within a total price range.
    
    Args:
        page: The Playwright page object.
        min_total: Minimum grand total.
        max_total: Maximum grand total.
    
    Usage Log:
    - Find high-value or low-value orders
    """
    import re
    await page.goto("/admin/sales/order")
    await page.get_by_role("button", name=re.compile(r"Filters")).click()
    
    total_group = page.get_by_role("group", name="Grand Total (Base)")
    await total_group.get_by_role("textbox", name="from").fill(str(min_total))
    await total_group.get_by_role("textbox", name="to").fill(str(max_total))
    
    await page.get_by_role("button", name="Apply Filters").click()


async def export_orders(page):
    """
    Export the current order list to a file.
    
    Args:
        page: The Playwright page object.
    
    Usage Log:
    - Export filtered order data for analysis
    """
    import re
    await page.goto("/admin/sales/order")
    await page.get_by_role("button", name=re.compile(r"Export", re.I)).click()


# ============================================================================
# BULK OPERATIONS SKILLS
# ============================================================================

async def bulk_update_product_status(page, status, product_names):
    """
    Update status for multiple products at once.
    
    Args:
        page: The Playwright page object.
        status: Status to set (e.g., "Enabled", "Disabled").
        product_names: List of product names to update.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    
    # Select each product
    for product_name in product_names:
        await page.get_by_role("checkbox").filter(has=page.get_by_text(product_name)).check()
    
    # Apply bulk action
    await page.get_by_role("combobox", name="Actions").select_option("Update attributes")
    await page.get_by_role("button", name="Submit").click()
    
    await page.get_by_role("combobox", name="Status").select_option(status)
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def bulk_delete_products(page, product_names):
    """
    Delete multiple products at once.
    
    Args:
        page: The Playwright page object.
        product_names: List of product names to delete.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    
    # Select each product
    for product_name in product_names:
        await page.get_by_role("checkbox").filter(has=page.get_by_text(product_name)).check()
    
    # Apply bulk delete
    await page.get_by_role("combobox", name="Actions").select_option("Delete")
    await page.get_by_role("button", name="Submit").click()
    await page.get_by_role("button", name=re.compile(r"OK|Confirm")).click()


# ============================================================================
# ADVANCED PRODUCT SKILLS
# ============================================================================

async def add_product_image(page, product_name, image_path):
    """
    Add an image to a product.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product.
        image_path: Path to the image file.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("button", name="Images").click()
    await page.set_input_files("input[type='file']", image_path)
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def set_product_description(page, product_name, description):
    """
    Set or update a product's description.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product.
        description: Product description text.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("textbox", name="Description").fill(description)
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def set_product_weight(page, product_name, weight):
    """
    Set a product's weight for shipping calculations.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product.
        weight: Weight value.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("textbox", name="Weight").fill(str(weight))
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def set_special_price(page, product_name, special_price, from_date=None, to_date=None):
    """
    Set a special/sale price for a product with optional date range.
    
    Args:
        page: The Playwright page object.
        product_name: Name of the product.
        special_price: Special price value.
        from_date: Optional start date for special price.
        to_date: Optional end date for special price.
    
    Usage Log:
    - Initial implementation, needs testing
    """
    import re
    
    await page.goto("/admin/catalog/product")
    await page.get_by_role("textbox", name="Name").fill(product_name)
    await page.get_by_role("button", name="Search").click()
    
    await page.get_by_role("link", name=product_name).first.click()
    
    await page.get_by_role("textbox", name="Special Price").fill(str(special_price))
    
    if from_date:
        await page.get_by_role("textbox", name="Special Price From").fill(from_date)
    if to_date:
        await page.get_by_role("textbox", name="Special Price To").fill(to_date)
    
    await page.get_by_role("button", name=re.compile(r"Save")).click()


async def get_orders_by_month(page, from_date, to_date, status="Complete"):
    """
    Get monthly order counts for a date range and status.
    
    Filters the orders grid by date range and status, then counts orders per month
    by parsing the Purchase Date column. Returns a dict mapping month "MM" -> count.
    
    Args:
        page: The Playwright page object.
        from_date: Start date in MM/DD/YYYY format.
        to_date: End date in MM/DD/YYYY format.
        status: Order status to filter (default "Complete").
    
    Usage Log:
    - Useful for reporting tasks (e.g., Feb–Nov 2022 counts in MM:COUNT format)
    - Handles column reordering by locating the "Purchase Date" header dynamically
    """
    import re
    from collections import defaultdict
    
    # Ensure we're on the orders page, then apply filters
    await page.goto("/admin/sales/order")
    await filter_orders_by_date_and_status(page, from_date, to_date, status)
    
    # Locate the orders table via its headers
    table = page.get_by_role("table").filter(
        has=page.get_by_role("columnheader", name=re.compile(r"Purchase Date", re.I))
    ).first
    
    headers = await table.get_by_role("columnheader").all_text_contents()
    date_idx = None
    for i, h in enumerate(headers):
        if h and re.search(r"purchase\s*date", h, re.I):
            date_idx = i
            break
    if date_idx is None:
        date_idx = 2  # Fallback if header detection fails
    
    monthly_counts = defaultdict(int)
    rows = await table.get_by_role("row").all()
    for row in rows[1:]:  # Skip header
        cells = await row.get_by_role("cell").all()
        if len(cells) > date_idx:
            txt = (await cells[date_idx].text_content()) or ""
            txt = txt.strip()
            if "/" in txt:
                # Format: MM/DD/YYYY ...
                date_part = txt.split()[0]
                mm = date_part.split("/")[0].zfill(2)
                monthly_counts[mm] += 1
            else:
                # Format with month names, e.g., "Nov 20, 2022 ..."
                abbr = txt[:3]
                map_mm = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
                          "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
                if abbr in map_mm:
                    monthly_counts[map_mm[abbr]] += 1
    
    return dict(monthly_counts)
