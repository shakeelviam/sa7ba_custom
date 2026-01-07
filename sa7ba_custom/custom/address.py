import frappe
from frappe import _

def validate_address(doc, method):
    """Validate address data"""
    # Ensure delivery area is selected for Kuwait addresses
    if doc.country == "Kuwait" and not doc.custom_delivery_area:
        frappe.throw(_("Delivery area is required for Kuwait addresses"))

def before_save_address(doc, method):
    """Auto-set delivery area based on area code in address"""
    if not doc.custom_delivery_area and doc.address_line1:
        # Try to extract area from address
        area_match = extract_area_from_address(doc.address_line1)
        if area_match:
            area = frappe.db.exists("Delivery Area", {"area_name": ["like", f"%{area_match}%"]})
            if area:
                doc.custom_delivery_area = area

def extract_area_from_address(address):
    """Simple area extraction logic for Kuwait addresses"""
    kuwait_areas = [
        "Jabriya", "Salmiya", "Hawally", "Farwaniya", 
        "Asimah", "Mubarak", "Ahmadi", "Jahra",
        "Salwa", "Mangaf", "Fahaheel", "Khaitan",
        "Rai", "Shuwaikh", "Sharq", "Mahboula",
        "Sabah Al-Salem", "Abdullah Al-Salem", "Adailiya",
        "Bneid Al-Qar", "Daiya", "Dasma", "Jibla"
    ]
    
    address_lower = address.lower()
    for area in kuwait_areas:
        if area.lower() in address_lower:
            return area
    
    return None

def get_delivery_areas_list():
    """Get list of active delivery areas"""
    return frappe.get_all("Delivery Area",
        filters={"is_active": 1},
        fields=["area_code", "area_name", "delivery_charge", "estimated_delivery_time"],
        order_by="area_name"
    )

def validate_delivery_area_availability(area_code):
    """Check if delivery area is available and active"""
    if not area_code:
        return False
    
    area = frappe.db.exists("Delivery Area", {
        "area_code": area_code,
        "is_active": 1
    })
    
    return bool(area)

def get_delivery_charge_for_area(area_code):
    """Get delivery charge for specific area"""
    if not area_code:
        return 0
    
    charge = frappe.db.get_value("Delivery Area", 
                                {"area_code": area_code, "is_active": 1}, 
                                "delivery_charge")
    return float(charge) if charge else 0

def update_address_delivery_area(doc, method):
    """Update delivery area when address is modified"""
    if doc.has_value_changed("address_line1"):
        # Try to auto-detect delivery area from address
        area_match = extract_area_from_address(doc.address_line1)
        if area_match:
            area = frappe.db.exists("Delivery Area", {"area_name": ["like", f"%{area_match}%"]})
            if area and area != doc.custom_delivery_area:
                doc.custom_delivery_area = area
                frappe.msgprint(_("Delivery area automatically set to {0}").format(area))
