# SA7BA Custom App Hooks
# ERPNext v15 + Webshop App Integration

app_name = "sa7ba_custom"
app_title = "SA7BA Custom"
app_publisher = "SA7BA"
app_description = "Guest Checkout & Area-Based Delivery Charges for SA7BA.com"
app_icon = "octicon octicon-package"
app_color = "grey"
app_version = "1.0.0"
app_license = "MIT"

# Required Apps
required_apps = ["erpnext", "webshop"]

# Doctype Events
doc_events = {
    "Customer": {
        "validate": "sa7ba_custom.customer.validate_customer",
        "on_update": "sa7ba_custom.customer.update_guest_count",
    },
    "Sales Order": {
        "validate": "sa7ba_custom.sales_order.validate_sales_order",
        "before_submit": "sa7ba_custom.sales_order.before_submit_sales_order",
        "before_insert": "sa7ba_custom.sales_order.before_insert_sales_order",
    },
    "Address": {
        "validate": "sa7ba_custom.address.validate_address",
        "before_save": "sa7ba_custom.address.before_save_address",
    },
    "Shopping Cart": {
        "before_add_to_cart": "sa7ba_custom.cart.before_add_to_cart",
        "calculate_cart_total": "sa7ba_custom.cart.calculate_cart_total",
    }
}

# API Whitelist
whitelisted_methods = [
    "sa7ba_custom.api.process_guest_checkout",
    "sa7ba_custom.api.get_delivery_areas",
    "sa7ba_custom.api.update_cart_delivery",
    "sa7ba_custom.api.validate_guest_info",
]

# Template Overrides
override_doctype_class = {
    "Shopping Cart": "sa7ba_custom.overrides.cart.CustomShoppingCart",
}

# Website Context
website_context = {
    "allow_guest_checkout": True,
    "delivery_areas": "sa7ba_custom.api.get_delivery_areas",
}

# App Include JS/CSS
app_include_js = "/assets/sa7ba_custom/js/delivery_area.js"
app_include_css = "/assets/sa7ba_custom/css/sa7ba_custom.css"

# Custom Fields
custom_fields = {
    "Customer": [
        {
            "fieldname": "custom_is_guest_customer",
            "label": "Is Guest Customer",
            "fieldtype": "Check",
            "default": 0,
            "description": "Customer without User account",
            "insert_after": "customer_group"
        },
        {
            "fieldname": "custom_guest_checkout_count",
            "label": "Guest Checkout Count",
            "fieldtype": "Int",
            "default": 0,
            "read_only": 1,
            "insert_after": "custom_is_guest_customer"
        }
    ],
    "Sales Order": [
        {
            "fieldname": "custom_is_guest_order",
            "label": "Is Guest Order",
            "fieldtype": "Check",
            "default": 0,
            "insert_after": "customer"
        },
        {
            "fieldname": "custom_guest_email",
            "label": "Guest Email",
            "fieldtype": "Data",
            "options": "Email",
            "insert_after": "custom_is_guest_order"
        },
        {
            "fieldname": "custom_guest_phone",
            "label": "Guest Phone",
            "fieldtype": "Data",
            "insert_after": "custom_guest_email"
        }
    ],
    "Address": [
        {
            "fieldname": "custom_delivery_area",
            "label": "Delivery Area",
            "fieldtype": "Link",
            "options": "Delivery Area",
            "reqd": 1,
            "insert_after": "city"
        }
    ],
    "Sales Order Item": [
        {
            "fieldname": "custom_is_delivery_charge",
            "label": "Is Delivery Charge",
            "fieldtype": "Check",
            "default": 0,
            "insert_after": "description"
        }
    ]
}

# Standard Reports
standard_reports = [
    {"report_name": "Delivery Charges Summary", "ref_doctype": "Sales Order"}
]

# Data Migration
data_migration = {
    "Delivery Area": {
        "source": "sa7ba_custom.setup_data.delivery_areas"
    }
}
