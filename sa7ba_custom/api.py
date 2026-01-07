import frappe
from frappe import _
import json

@frappe.whitelist(allow_guest=True)
def process_guest_checkout(cart_data, guest_info):
    """
    Process guest checkout - called from frontend
    Returns: customer_id, order_id, or error
    """
    try:
        # Validate inputs
        if not guest_info.get('email') or not guest_info.get('phone'):
            frappe.throw("Email and phone are required")
        
        # Validate guest info
        validate_guest_info(guest_info)
        
        # Create/retrieve guest customer
        from sa7ba_custom.sa7ba_custom.custom.customer import create_guest_customer, set_guest_customer_session
        customer_id = create_guest_customer(
            email=guest_info['email'],
            phone=guest_info['phone'],
            first_name=guest_info.get('first_name', 'Guest'),
            last_name=guest_info.get('last_name', '')
        )
        
        # Add customer to session for Webshop
        set_guest_customer_session(customer_id)
        
        return {
            "success": True,
            "customer_id": customer_id,
            "message": "Guest customer created successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Guest checkout failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist(allow_guest=True)
def get_delivery_areas():
    """Return all active delivery areas"""
    areas = frappe.get_all("Delivery Area",
        filters={"is_active": 1},
        fields=["area_code", "area_name", "delivery_charge", 
                "estimated_delivery_time", "notes"],
        order_by="area_name"
    )
    return areas

@frappe.whitelist(allow_guest=True)
def update_cart_delivery(area_code, delivery_charge):
    """Update cart with delivery charge"""
    try:
        # Validate area code
        if not area_code:
            return {
                "success": False,
                "error": "Area code is required"
            }
        
        # Check if area exists and is active
        area = frappe.db.exists("Delivery Area", {
            "area_code": area_code,
            "is_active": 1
        })
        
        if not area:
            return {
                "success": False,
                "error": "Invalid or inactive delivery area"
            }
        
        # Get current cart
        from webshop.webshop.doctype.webshop_settings.webshop_cart import get_cart
        cart = get_cart()
        
        # Update with delivery charge
        from sa7ba_custom.sa7ba_custom.custom.cart import CustomShoppingCart
        cart_manager = CustomShoppingCart()
        updated_cart = cart_manager.update_cart_with_delivery(cart, area_code)
        
        # Save updated cart
        frappe.local.cookie_manager.set_cookie('cart', json.dumps(updated_cart))
        frappe.local.cookie_manager.set_cookie('selected_delivery_area', area_code)
        
        return {
            "success": True,
            "message": "Cart updated with delivery charge",
            "delivery_charge": delivery_charge,
            "cart_total": updated_cart.get("total", 0)
        }
    except Exception as e:
        frappe.log_error(f"Cart update failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist(allow_guest=True)
def validate_guest_info(guest_info):
    """Validate guest checkout information"""
    errors = []
    
    # Validate email
    if not guest_info.get('email'):
        errors.append("Email is required")
    elif '@' not in guest_info.get('email', ''):
        errors.append("Invalid email format")
    
    # Validate phone
    if not guest_info.get('phone'):
        errors.append("Phone is required")
    elif len(guest_info.get('phone', '')) < 8:
        errors.append("Phone number is too short")
    
    # Validate name
    if not guest_info.get('first_name'):
        errors.append("First name is required")
    
    if errors:
        frappe.throw("<br>".join(errors))

@frappe.whitelist(allow_guest=True)
def get_cart_summary():
    """Get cart summary with delivery information"""
    try:
        from webshop.webshop.doctype.webshop_settings.webshop_cart import get_cart
        from sa7ba_custom.sa7ba_custom.custom.cart import CustomShoppingCart
        
        cart = get_cart()
        cart_manager = CustomShoppingCart()
        summary = cart_manager.get_cart_summary(cart)
        
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        frappe.log_error(f"Cart summary failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist(allow_guest=True)
def remove_delivery_charge():
    """Remove delivery charge from cart"""
    try:
        from webshop.webshop.doctype.webshop_settings.webshop_cart import get_cart
        from sa7ba_custom.sa7ba_custom.custom.cart import CustomShoppingCart
        
        cart = get_cart()
        cart_manager = CustomShoppingCart()
        updated_cart = cart_manager.remove_delivery_charge(cart)
        
        # Save updated cart
        frappe.local.cookie_manager.set_cookie('cart', json.dumps(updated_cart))
        frappe.local.cookie_manager.delete_cookie('selected_delivery_area')
        
        return {
            "success": True,
            "message": "Delivery charge removed from cart",
            "cart_total": updated_cart.get("total", 0)
        }
    except Exception as e:
        frappe.log_error(f"Remove delivery charge failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist(allow_guest=True)
def check_delivery_availability(area_code):
    """Check if delivery is available for the area"""
    try:
        from sa7ba_custom.sa7ba_custom.custom.address import validate_delivery_area_availability, get_delivery_charge_for_area
        
        is_available = validate_delivery_area_availability(area_code)
        charge = get_delivery_charge_for_area(area_code) if is_available else 0
        
        return {
            "success": True,
            "available": is_available,
            "delivery_charge": charge
        }
    except Exception as e:
        frappe.log_error(f"Delivery availability check failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
