import frappe
from frappe import _

def create_delivery_areas():
    """Create initial delivery areas for Kuwait"""
    
    delivery_areas = [
        {
            "area_code": "JAB",
            "area_name": "Al Jabriya",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Central Kuwait area with good accessibility"
        },
        {
            "area_code": "SAL",
            "area_name": "Salmiya",
            "delivery_charge": 3.000,
            "estimated_delivery_time": "2-3 hours",
            "is_active": 1,
            "notes": "Eastern coastal area, moderate traffic"
        },
        {
            "area_code": "HAW",
            "area_name": "Hawally",
            "delivery_charge": 2.500,
            "estimated_delivery_time": "2-3 hours",
            "is_active": 1,
            "notes": "Commercial and residential area"
        },
        {
            "area_code": "FAI",
            "area_name": "Al Farwaniya",
            "delivery_charge": 3.500,
            "estimated_delivery_time": "3-4 hours",
            "is_active": 1,
            "notes": "Southern residential area"
        },
        {
            "area_code": "ASI",
            "area_name": "Al Asimah (Kuwait City)",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Central business district"
        },
        {
            "area_code": "MUB",
            "area_name": "Mubarak Al-Kabeer",
            "delivery_charge": 3.000,
            "estimated_delivery_time": "2-3 hours",
            "is_active": 1,
            "notes": "Eastern residential area"
        },
        {
            "area_code": "AHA",
            "area_name": "Al Ahmadi",
            "delivery_charge": 4.000,
            "estimated_delivery_time": "3-5 hours",
            "is_active": 1,
            "notes": "Southern industrial and residential area"
        },
        {
            "area_code": "JAH",
            "area_name": "Al Jahra",
            "delivery_charge": 5.000,
            "estimated_delivery_time": "4-6 hours",
            "is_active": 1,
            "notes": "Northern residential area, far from city center"
        },
        {
            "area_code": "SALW",
            "area_name": "Salwa",
            "delivery_charge": 3.500,
            "estimated_delivery_time": "3-4 hours",
            "is_active": 1,
            "notes": "Southern residential area"
        },
        {
            "area_code": "MAN",
            "area_name": "Mangaf",
            "delivery_charge": 3.500,
            "estimated_delivery_time": "3-4 hours",
            "is_active": 1,
            "notes": "Southern residential area"
        },
        {
            "area_code": "FAH",
            "area_name": "Fahaheel",
            "delivery_charge": 3.000,
            "estimated_delivery_time": "2-3 hours",
            "is_active": 1,
            "notes": "Coastal commercial area"
        },
        {
            "area_code": "KHA",
            "area_name": "Khaitan",
            "delivery_charge": 3.500,
            "estimated_delivery_time": "3-4 hours",
            "is_active": 1,
            "notes": "Southern residential area"
        },
        {
            "area_code": "RAI",
            "area_name": "Al Rai",
            "delivery_charge": 2.500,
            "estimated_delivery_time": "2-3 hours",
            "is_active": 1,
            "notes": "Industrial and commercial area"
        },
        {
            "area_code": "SHW",
            "area_name": "Shuwaikh",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Industrial and port area"
        },
        {
            "area_code": "SHA",
            "area_name": "Sharq",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Central commercial area"
        },
        {
            "area_code": "MAH",
            "area_name": "Mahboula",
            "delivery_charge": 4.000,
            "estimated_delivery_time": "3-5 hours",
            "is_active": 1,
            "notes": "Southern residential area"
        },
        {
            "area_code": "SAB",
            "area_name": "Sabah Al-Salem",
            "delivery_charge": 3.500,
            "estimated_delivery_time": "3-4 hours",
            "is_active": 1,
            "notes": "Southern residential area"
        },
        {
            "area_code": "ABD",
            "area_name": "Abdullah Al-Salem",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Central residential area"
        },
        {
            "area_code": "ADA",
            "area_name": "Adailiya",
            "delivery_charge": 2.500,
            "estimated_delivery_time": "2-3 hours",
            "is_active": 1,
            "notes": "Central residential area"
        },
        {
            "area_code": "BNE",
            "area_name": "Bneid Al-Qar",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Central commercial area"
        },
        {
            "area_code": "DAI",
            "area_name": "Daiya",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Central residential area"
        },
        {
            "area_code": "DAS",
            "area_name": "Dasma",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Central residential area"
        },
        {
            "area_code": "JIB",
            "area_name": "Jibla",
            "delivery_charge": 2.000,
            "estimated_delivery_time": "1-2 hours",
            "is_active": 1,
            "notes": "Central residential area"
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for area_data in delivery_areas:
        # Check if area already exists
        existing_area = frappe.db.exists("Delivery Area", {"area_code": area_data["area_code"]})
        
        if existing_area:
            # Update existing area
            area = frappe.get_doc("Delivery Area", existing_area)
            for key, value in area_data.items():
                if area.has_value_changed(key) and hasattr(area, key):
                    setattr(area, key, value)
            area.save(ignore_permissions=True)
            updated_count += 1
            frappe.logger().info(f"Updated delivery area: {area_data['area_name']}")
        else:
            # Create new area
            area = frappe.new_doc("Delivery Area")
            for key, value in area_data.items():
                setattr(area, key, value)
            area.insert(ignore_permissions=True)
            created_count += 1
            frappe.logger().info(f"Created delivery area: {area_data['area_name']}")
    
    frappe.db.commit()
    
    return {
        "created": created_count,
        "updated": updated_count,
        "total": created_count + updated_count
    }

def create_delivery_charge_item():
    """Create the delivery charge item"""
    
    item_code = "DELIVERY-CHARGE"
    
    # Check if item already exists
    if frappe.db.exists("Item", item_code):
        frappe.logger().info(f"Delivery charge item {item_code} already exists")
        return item_code
    
    # Create new item
    item = frappe.new_doc("Item")
    item.item_code = item_code
    item.item_name = "Delivery Charge"
    item.item_group = "Services"
    item.description = "Area-based delivery service charge"
    item.stock_uom = "Nos"
    item.is_stock_item = 0
    item.include_item_in_manufacturing = 0
    item.show_in_website = 1
    item.enabled = 1
    
    # Set default warehouse (optional for service item)
    item.default_warehouse = "Stores - SA"
    
    item.insert(ignore_permissions=True)
    
    frappe.logger().info(f"Created delivery charge item: {item_code}")
    return item_code

def setup_initial_data():
    """Setup all initial data for the app"""
    
    try:
        # Create delivery areas
        areas_result = create_delivery_areas()
        frappe.logger().info(f"Delivery areas setup: {areas_result}")
        
        # Create delivery charge item
        item_code = create_delivery_charge_item()
        frappe.logger().info(f"Delivery charge item created: {item_code}")
        
        return {
            "success": True,
            "areas": areas_result,
            "item": item_code,
            "message": "Initial data setup completed successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Initial data setup failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Initial data setup failed"
        }
