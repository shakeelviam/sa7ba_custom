import frappe
from frappe import _
import json

class CustomShoppingCart:
    def __init__(self):
        self.delivery_charge_item = "DELIVERY-CHARGE"
    
    def get_delivery_charge(self, area_code):
        """Get delivery charge for area"""
        if not area_code:
            return 0
        
        charge = frappe.db.get_value("Delivery Area", 
                                    {"area_code": area_code, "is_active": 1}, 
                                    "delivery_charge")
        return float(charge) if charge else 0
    
    def update_cart_with_delivery(self, cart, area_code):
        """Add delivery charge to cart"""
        delivery_charge = self.get_delivery_charge(area_code)
        
        # Remove any existing delivery charge
        cart["items"] = [item for item in cart.get("items", []) 
                        if item.get("item_code") != self.delivery_charge_item]
        
        # Add delivery charge item
        if delivery_charge > 0:
            cart["items"].append({
                "item_code": self.delivery_charge_item,
                "item_name": f"Delivery Service Charge",
                "qty": 1,
                "rate": delivery_charge,
                "amount": delivery_charge,
                "description": f"Delivery to {area_code} area",
                "custom_is_delivery_charge": 1
            })
        
        # Recalculate totals
        cart = self.calculate_cart_total(cart)
        return cart
    
    def calculate_cart_total(self, cart):
        """Calculate cart total including delivery charges"""
        total = 0
        for item in cart.get("items", []):
            total += item.get("amount", 0)
        
        cart["total"] = total
        cart["formatted_total"] = f"KWD {total:.3f}"
        
        return cart
    
    def before_add_to_cart(self, cart, item_code, qty):
        """Before adding item to cart"""
        # Check if delivery area is selected
        selected_area = frappe.local.cookie_manager.get_cookie('selected_delivery_area')
        if not selected_area:
            # Don't block adding items, but remind user to select area
            pass
    
    def remove_delivery_charge(self, cart):
        """Remove delivery charge from cart"""
        cart["items"] = [item for item in cart.get("items", []) 
                        if item.get("item_code") != self.delivery_charge_item]
        return self.calculate_cart_total(cart)
    
    def get_cart_summary(self, cart):
        """Get cart summary with delivery info"""
        summary = {
            "items_count": len(cart.get("items", [])),
            "subtotal": 0,
            "delivery_charge": 0,
            "total": 0,
            "delivery_area": None
        }
        
        # Get selected delivery area
        selected_area = frappe.local.cookie_manager.get_cookie('selected_delivery_area')
        if selected_area:
            summary["delivery_area"] = selected_area
            summary["delivery_charge"] = self.get_delivery_charge(selected_area)
        
        # Calculate subtotal (excluding delivery charges)
        for item in cart.get("items", []):
            if item.get("item_code") != self.delivery_charge_item:
                summary["subtotal"] += item.get("amount", 0)
            else:
                summary["delivery_charge"] = item.get("amount", 0)
        
        summary["total"] = summary["subtotal"] + summary["delivery_charge"]
        
        return summary

def calculate_cart_total(cart):
    """Override cart calculation"""
    cart_manager = CustomShoppingCart()
    return cart_manager.calculate_cart_total(cart)

def before_add_to_cart(cart, item_code, qty):
    """Hook for before adding to cart"""
    cart_manager = CustomShoppingCart()
    return cart_manager.before_add_to_cart(cart, item_code, qty)
