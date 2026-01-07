import frappe
from frappe import _
from frappe.utils import validate_email_address, validate_phone_number

def validate_customer(doc, method):
    """Validate customer data"""
    if doc.custom_is_guest_customer and not doc.email_id:
        frappe.throw(_("Guest customers must have an email address"))
    
    if doc.custom_is_guest_customer and not doc.mobile_no:
        frappe.throw(_("Guest customers must have a mobile number"))

def update_guest_count(doc, method):
    """Update guest checkout count"""
    if doc.custom_is_guest_customer and doc.has_value_changed('custom_is_guest_customer'):
        # Increment guest checkout count
        doc.custom_guest_checkout_count = (doc.custom_guest_checkout_count or 0) + 1

def create_guest_customer(email, phone, first_name, last_name=""):
    """
    Create or retrieve guest customer
    Strategy: Use email as primary identifier, phone as secondary
    """
    # Validate inputs
    if not email:
        frappe.throw(_("Email is required for guest checkout"))
    
    if not phone:
        frappe.throw(_("Phone is required for guest checkout"))
    
    # Validate email format
    if not validate_email_address(email):
        frappe.throw(_("Invalid email address"))
    
    # Validate phone format (Kuwait mobile numbers: 5xxxxxxx or 6xxxxxxx)
    if not validate_phone_number(phone):
        frappe.throw(_("Invalid phone number"))
    
    # 1. Check if customer exists by email
    existing_customer = frappe.db.exists("Customer", {"email_id": email})
    
    if existing_customer:
        customer = frappe.get_doc("Customer", existing_customer)
        # Update phone if different
        if phone and customer.mobile_no != phone:
            customer.mobile_no = phone
            customer.save(ignore_permissions=True)
        
        # Update guest status if not set
        if not customer.custom_is_guest_customer:
            customer.custom_is_guest_customer = 1
            customer.save(ignore_permissions=True)
        
        return customer.name
    
    # 2. Check by phone if no email match
    if phone:
        existing_by_phone = frappe.db.exists("Customer", {"mobile_no": phone})
        if existing_by_phone:
            customer = frappe.get_doc("Customer", existing_by_phone)
            # Update email if different
            if email and customer.email_id != email:
                customer.email_id = email
                customer.save(ignore_permissions=True)
            
            # Update guest status if not set
            if not customer.custom_is_guest_customer:
                customer.custom_is_guest_customer = 1
                customer.save(ignore_permissions=True)
            
            return customer.name
    
    # 3. Create new guest customer
    customer = frappe.new_doc("Customer")
    customer.customer_name = f"{first_name} {last_name}".strip() if last_name else first_name
    customer.customer_type = "Individual"
    customer.customer_group = "Individual"  # From ERPNext setup
    customer.territory = "Kuwait"
    customer.email_id = email
    customer.mobile_no = phone
    customer.custom_is_guest_customer = 1
    customer.custom_guest_checkout_count = 1
    
    # Set naming series for guest customers
    customer.naming_series = "GST-.#####"
    
    customer.insert(ignore_permissions=True)
    
    return customer.name

def get_guest_customer_by_session():
    """Get guest customer from session"""
    guest_customer_id = frappe.local.cookie_manager.get_cookie('guest_customer_id')
    if guest_customer_id:
        return frappe.db.exists("Customer", guest_customer_id)
    return None

def set_guest_customer_session(customer_id):
    """Set guest customer in session"""
    frappe.local.cookie_manager.set_cookie('guest_customer_id', customer_id)

def clear_guest_customer_session():
    """Clear guest customer from session"""
    frappe.local.cookie_manager.delete_cookie('guest_customer_id')
