import frappe
from frappe import _

def execute(filters=None):
    """Execute the delivery charges summary report"""
    
    columns = [
        {"fieldname": "delivery_area", "label": "Delivery Area", "width": 150},
        {"fieldname": "area_code", "label": "Area Code", "width": 100},
        {"fieldname": "order_count", "label": "Order Count", "width": 100, "fieldtype": "Int"},
        {"fieldname": "total_delivery_charges", "label": "Total Delivery Charges", "width": 150, "fieldtype": "Currency"},
        {"fieldname": "average_order_value", "label": "Avg Order Value", "width": 150, "fieldtype": "Currency"},
        {"fieldname": "delivery_charge_rate", "label": "Delivery Rate", "width": 120, "fieldtype": "Currency"},
        {"fieldname": "estimated_delivery_time", "label": "Est. Delivery Time", "width": 120}
    ]
    
    data = get_delivery_charges_data(filters)
    
    return columns, data

def get_delivery_charges_data(filters):
    """Get delivery charges data from sales orders"""
    
    # Get date range from filters
    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None
    
    # Build query conditions
    conditions = ["so.docstatus = 1"]
    if from_date:
        conditions.append(f"so.transaction_date >= '{from_date}'")
    if to_date:
        conditions.append(f"so.transaction_date <= '{to_date}'")
    
    where_clause = " AND ".join(conditions)
    
    query = f"""
        SELECT 
            da.area_name as delivery_area,
            da.area_code,
            COUNT(DISTINCT so.name) as order_count,
            COALESCE(SUM(soi.amount), 0) as total_delivery_charges,
            COALESCE(AVG(so.grand_total), 0) as average_order_value,
            da.delivery_charge as delivery_charge_rate,
            da.estimated_delivery_time
        FROM `tabDelivery Area` da
        LEFT JOIN `tabAddress` addr ON addr.custom_delivery_area = da.name
        LEFT JOIN `tabSales Order` so ON so.shipping_address_name = addr.name AND {where_clause}
        LEFT JOIN `tabSales Order Item` soi ON soi.parent = so.name AND soi.item_code = 'DELIVERY-CHARGE'
        WHERE da.is_active = 1
        GROUP BY da.name, da.area_name, da.area_code, da.delivery_charge, da.estimated_delivery_time
        ORDER BY da.area_name
    """
    
    data = frappe.db.sql(query, as_dict=True)
    
    # Format currency values
    for row in data:
        row["total_delivery_charges"] = float(row["total_delivery_charges"] or 0)
        row["average_order_value"] = float(row["average_order_value"] or 0)
        row["delivery_charge_rate"] = float(row["delivery_charge_rate"] or 0)
    
    return data

def get_report_summary(filters):
    """Get report summary"""
    
    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None
    
    conditions = ["so.docstatus = 1"]
    if from_date:
        conditions.append(f"so.transaction_date >= '{from_date}'")
    if to_date:
        conditions.append(f"so.transaction_date <= '{to_date}'")
    
    where_clause = " AND ".join(conditions)
    
    summary_query = f"""
        SELECT 
            COUNT(DISTINCT so.name) as total_orders,
            COUNT(DISTINCT CASE WHEN so.custom_is_guest_order = 1 THEN so.name END) as guest_orders,
            COALESCE(SUM(soi.amount), 0) as total_delivery_charges,
            COALESCE(AVG(so.grand_total), 0) as avg_order_value
        FROM `tabSales Order` so
        LEFT JOIN `tabSales Order Item` soi ON soi.parent = so.name AND soi.item_code = 'DELIVERY-CHARGE'
        WHERE {where_clause}
    """
    
    summary = frappe.db.sql(summary_query, as_dict=True)
    
    if summary:
        summary_data = summary[0]
        return [
            {"value": summary_data.get("total_orders", 0), "label": "Total Orders", "datatype": "Int"},
            {"value": summary_data.get("guest_orders", 0), "label": "Guest Orders", "datatype": "Int"},
            {"value": summary_data.get("total_delivery_charges", 0), "label": "Total Delivery Revenue", "datatype": "Currency"},
            {"value": summary_data.get("avg_order_value", 0), "label": "Avg Order Value", "datatype": "Currency"}
        ]
    
    return []

# Report configuration
report_config = {
    "doctype": "Report",
    "report_name": "Delivery Charges Summary",
    "report_type": "Script Report",
    "ref_doctype": "Sales Order",
    "is_standard": "No",
    "add_total_row": 1,
    "sort_by": "Total Delivery Charges",
    "sort_order": "desc"
}
