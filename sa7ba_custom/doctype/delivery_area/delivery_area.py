import frappe
from frappe import _

class DeliveryArea:
    def validate(self):
        """Validate delivery area data"""
        if self.delivery_charge <= 0:
            frappe.throw(_("Delivery charge must be greater than 0"))
        
        if not self.area_code:
            frappe.throw(_("Area code is required"))
        
        if not self.area_name:
            frappe.throw(_("Area name is required"))

    def on_update(self):
        """Update related data when delivery area changes"""
        self.update_cart_charges()

    def update_cart_charges(self):
        """Update existing carts if delivery charge changes"""
        # This would be called if delivery charges are updated
        # Implementation depends on cart persistence strategy
        pass

    @frappe.whitelist()
    def get_orders_count(self):
        """Get number of orders for this delivery area"""
        return frappe.db.count("Sales Order", {
            "shipping_address.custom_delivery_area": self.name,
            "docstatus": ["!=", 2]
        })

    @frappe.whitelist()
    def get_total_revenue(self):
        """Get total revenue from this delivery area"""
        result = frappe.db.sql("""
            SELECT SUM(grand_total) as total_revenue
            FROM `tabSales Order`
            WHERE shipping_address_name IN (
                SELECT name FROM `tabAddress` 
                WHERE custom_delivery_area = %s
            )
            AND docstatus = 1
        """, self.name, as_dict=True)
        
        return result[0].total_revenue if result and result[0].total_revenue else 0
