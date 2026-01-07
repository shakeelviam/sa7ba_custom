import frappe
from frappe import _
import json

class CustomShoppingCart:
    """
    Override for Webshop Shopping Cart to handle area-based delivery charges
    """
    
    def __init__(self):
        self.delivery_charge_item = "DELIVERY-CHARGE"
    
    def get_cart(self):
        """Get current cart with delivery charge support"""
        from webshop.webshop.doctype.webshop_settings.webshop_cart import get_cart as original_get_cart
        cart = original_get_cart()
        
        # Add delivery charge if area is selected
        selected_area = frappe.local.cookie_manager.get_cookie('selected_delivery_area')
        if selected_area:
            cart = self.update_cart_with_delivery(cart, selected_area)
        
        return cart
    
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
    
    def get_delivery_charge(self, area_code):
        """Get delivery charge for area"""
        if not area_code:
            return 0
        
        charge = frappe.db.get_value("Delivery Area", 
                                    {"area_code": area_code, "is_active": 1}, 
                                    "delivery_charge")
        return float(charge) if charge else 0
    
    def calculate_cart_total(self, cart):
        """Calculate cart total including delivery charges"""
        from webshop.webshop.doctype.webshop_settings.webshop_cart import calculate_cart_total as original_calculate
        
        # Original calculation
        cart = original_calculate(cart)
        
        # Add delivery charge summary
        delivery_charge = 0
        for item in cart.get("items", []):
            if item.get("item_code") == self.delivery_charge_item:
                delivery_charge = item.get("amount", 0)
                break
        
        cart["delivery_charge"] = delivery_charge
        cart["subtotal_without_delivery"] = cart.get("total", 0) - delivery_charge
        
        return cart
    
    def add_to_cart(self, item_code, qty, with_items=False, additional_notes=None):
        """Override add to cart to handle delivery charges"""
        from webshop.webshop.doctype.webshop_settings.webshop_cart import add_to_cart as original_add_to_cart
        
        # Add item to cart
        result = original_add_to_cart(item_code, qty, with_items, additional_notes)
        
        # Update with delivery charge if area is selected
        selected_area = frappe.local.cookie_manager.get_cookie('selected_delivery_area')
        if selected_area:
            cart = self.get_cart()
            cart = self.update_cart_with_delivery(cart, selected_area)
            # Save updated cart
            frappe.local.cookie_manager.set_cookie('cart', json.dumps(cart))
        
        return result
    
    def remove_from_cart(self, item_code):
        """Override remove from cart to handle delivery charges"""
        from webshop.webshop.doctype.webshop_settings.webshop_cart import remove_from_cart as original_remove
        
        # Remove item from cart
        result = original_remove(item_code)
        
        # Update with delivery charge if area is selected
        selected_area = frappe.local.cookie_manager.get_cookie('selected_delivery_area')
        if selected_area:
            cart = self.get_cart()
            cart = self.update_cart_with_delivery(cart, selected_area)
            # Save updated cart
            frappe.local.cookie_manager.set_cookie('cart', json.dumps(cart))
        
        return result

# Override the original cart functions
def get_cart():
    """Override get_cart function"""
    cart_manager = CustomShoppingCart()
    return cart_manager.get_cart()

def calculate_cart_total(cart):
    """Override calculate_cart_total function"""
    cart_manager = CustomShoppingCart()
    return cart_manager.calculate_cart_total(cart)

def add_to_cart(item_code, qty, with_items=False, additional_notes=None):
    """Override add_to_cart function"""
    cart_manager = CustomShoppingCart()
    return cart_manager.add_to_cart(item_code, qty, with_items, additional_notes)

def remove_from_cart(item_code):
    """Override remove_from_cart function"""
    cart_manager = CustomShoppingCart()
    return cart_manager.remove_from_cart(item_code)
