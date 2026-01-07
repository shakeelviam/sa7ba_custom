import frappe
from frappe import _

def validate_sales_order(doc, method):
    """Validate sales order and ensure delivery charge is included"""
    
    # Skip if already has delivery charge
    has_delivery_charge = any(
        item.get("item_code") == "DELIVERY-CHARGE" 
        for item in doc.items
    )
    
    if has_delivery_charge:
        return
    
    # Get delivery area from shipping address
    if doc.shipping_address_name:
        address = frappe.get_doc("Address", doc.shipping_address_name)
        if address.custom_delivery_area:
            area = frappe.get_doc("Delivery Area", address.custom_delivery_area)
            
            # Add delivery charge item
            doc.append("items", {
                "item_code": "DELIVERY-CHARGE",
                "item_name": f"Delivery to {area.area_name}",
                "description": f"Delivery service charge for {area.area_name} area",
                "qty": 1,
                "uom": "Nos",
                "rate": area.delivery_charge,
                "amount": area.delivery_charge,
                "custom_is_delivery_charge": 1
            })
        else:
            frappe.throw("Delivery area is required. Please select a delivery area.")
    else:
        frappe.throw("Shipping address is required for delivery charge calculation.")

def before_submit_sales_order(doc, method):
    """Validate delivery charge before submission"""
    # Ensure delivery charge is present
    delivery_items = [item for item in doc.items 
                     if item.get("item_code") == "DELIVERY-CHARGE"]
    
    if not delivery_items:
        frappe.throw("Delivery charge must be included in the order")
    
    # Validate amount matches area charge
    if doc.shipping_address_name:
        address = frappe.get_doc("Address", doc.shipping_address_name)
        if address.custom_delivery_area:
            area = frappe.get_doc("Delivery Area", address.custom_delivery_area)
            delivery_charge_in_order = sum(item.amount for item in delivery_items)
            
            if float(delivery_charge_in_order) != float(area.delivery_charge):
                frappe.throw(
                    f"Delivery charge mismatch. Expected KWD {area.delivery_charge}, "
                    f"found KWD {delivery_charge_in_order}"
                )

def before_insert_sales_order(doc, method):
    """Handle guest customer assignment before sales order insertion"""
    if frappe.session.user == "Guest" and hasattr(doc, 'contact_email'):
        # This is a guest checkout
        doc.custom_is_guest_order = 1
        doc.custom_guest_email = doc.contact_email
        doc.custom_guest_phone = doc.contact_mobile
        
        # Ensure customer exists
        from sa7ba_custom.sa7ba_custom.custom.customer import create_guest_customer
        customer_name = create_guest_customer(
            email=doc.contact_email,
            phone=doc.contact_mobile,
            first_name=doc.contact_person or "Guest",
            last_name=""
        )
        
        doc.customer = customer_name
        
        # Set customer name if not set
        if not doc.customer_name:
            customer = frappe.get_doc("Customer", customer_name)
            doc.customer_name = customer.customer_name

def update_guest_order_stats(doc, method):
    """Update guest order statistics"""
    if doc.custom_is_guest_order:
        # Update customer's guest checkout count
        if doc.customer:
            frappe.db.set_value("Customer", doc.customer, "custom_guest_checkout_count", 
                              frappe.db.get_value("Customer", doc.customer, "custom_guest_checkout_count") + 1)

def on_submit_sales_order(doc, method):
    """Actions after sales order submission"""
    if doc.custom_is_guest_order:
        # Send order confirmation to guest customer
        send_guest_order_confirmation(doc)

def send_guest_order_confirmation(doc):
    """Send order confirmation to guest customer"""
    try:
        # Get email template or use default
        template = frappe.get_doc("Email Template", "Guest Order Confirmation")
        
        # Prepare context
        context = {
            "customer_name": doc.customer_name,
            "order_id": doc.name,
            "order_total": doc.grand_total,
            "delivery_address": doc.shipping_address_name,
            "guest_email": doc.custom_guest_email
        }
        
        # Send email
        frappe.sendmail(
            recipients=[doc.custom_guest_email],
            template=template.name,
            args=context,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
            send_priority=1
        )
        
    except Exception as e:
        frappe.log_error(f"Failed to send guest order confirmation: {str(e)}")
