/**
 * SA7BA Delivery Area Manager
 * Handles area-based delivery charges for guest checkout
 */

class DeliveryAreaManager {
    constructor() {
        this.areas = [];
        this.selectedArea = null;
        this.deliveryCharge = 0;
        this.cartTotal = 0;
        this.isInitialized = false;
    }
    
    async init() {
        if (this.isInitialized) return;
        
        try {
            await this.loadAreas();
            this.setupEventListeners();
            this.restoreSelectedArea();
            this.isInitialized = true;
        } catch (error) {
            console.error('Failed to initialize delivery area manager:', error);
        }
    }
    
    async loadAreas() {
        try {
            const response = await fetch('/api/method/sa7ba_custom.api.get_delivery_areas');
            const result = await response.json();
            
            if (result.success) {
                this.areas = result.message || [];
                this.renderAreaSelector();
            } else {
                throw new Error(result.error || 'Failed to load delivery areas');
            }
        } catch (error) {
            console.error('Failed to load delivery areas:', error);
            this.showError('Failed to load delivery areas. Please refresh the page.');
        }
    }
    
    renderAreaSelector() {
        const container = document.getElementById('delivery-area-container');
        if (!container) return;
        
        let html = `
            <div class="delivery-area-section mb-4">
                <h4 class="mb-3">Select Delivery Area *</h4>
                <p class="text-muted mb-3">Delivery charges apply to all orders</p>
                
                <div class="form-group">
                    <select class="form-control form-control-lg" id="delivery-area-select" required>
                        <option value="">-- Choose your area --</option>
        `;
        
        this.areas.forEach(area => {
            html += `
                <option value="${area.area_code}" 
                        data-charge="${area.delivery_charge}"
                        data-time="${area.estimated_delivery_time}">
                    ${area.area_name} - KWD ${parseFloat(area.delivery_charge).toFixed(3)} 
                    (${area.estimated_delivery_time})
                </option>
            `;
        });
        
        html += `
                    </select>
                </div>
                
                <div id="delivery-summary" class="mt-3 p-3 bg-light rounded" style="display: none;">
                    <div class="row">
                        <div class="col-md-6">
                            <strong>Delivery to:</strong> <span id="selected-area-name"></span>
                        </div>
                        <div class="col-md-6 text-end">
                            <strong>Charge:</strong> KWD <span id="delivery-charge-amount"></span>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-12">
                            <small class="text-muted">
                                <i class="fa fa-clock"></i> Estimated delivery: 
                                <span id="delivery-time"></span>
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    setupEventListeners() {
        const select = document.getElementById('delivery-area-select');
        if (select) {
            select.addEventListener('change', (e) => {
                this.handleAreaChange(e.target.value);
            });
        }
        
        // Handle cart page area selection
        const cartSelect = document.getElementById('cart-delivery-area');
        if (cartSelect) {
            cartSelect.addEventListener('change', (e) => {
                this.handleCartAreaChange(e.target.value);
            });
        }
    }
    
    handleAreaChange(areaCode) {
        const select = document.getElementById('delivery-area-select');
        const selectedOption = select.options[select.selectedIndex];
        
        if (!areaCode) {
            document.getElementById('delivery-summary').style.display = 'none';
            this.selectedArea = null;
            this.deliveryCharge = 0;
            return;
        }
        
        this.selectedArea = areaCode;
        this.deliveryCharge = parseFloat(selectedOption.dataset.charge) || 0;
        
        // Update UI
        document.getElementById('selected-area-name').textContent = selectedOption.text.split(' - ')[0];
        document.getElementById('delivery-charge-amount').textContent = this.deliveryCharge.toFixed(3);
        document.getElementById('delivery-time').textContent = selectedOption.dataset.time;
        document.getElementById('delivery-summary').style.display = 'block';
        
        // Update cart via API
        this.updateCartDeliveryCharge();
        
        // Store in session for persistence
        sessionStorage.setItem('selected_delivery_area', areaCode);
    }
    
    async handleCartAreaChange(areaCode) {
        if (!areaCode) {
            await this.removeDeliveryCharge();
            return;
        }
        
        const select = document.getElementById('cart-delivery-area');
        const selectedOption = select.options[select.selectedIndex];
        const charge = parseFloat(selectedOption.textContent.split('KWD ')[1]) || 0;
        
        try {
            const response = await fetch('/api/method/sa7ba_custom.api.update_cart_delivery', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Frappe-CSRF-Token': frappe.csrf_token
                },
                body: JSON.stringify({
                    area_code: areaCode,
                    delivery_charge: charge
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Refresh cart display
                this.refreshCartDisplay();
                sessionStorage.setItem('selected_delivery_area', areaCode);
            } else {
                this.showError(result.error || 'Failed to update cart');
            }
        } catch (error) {
            console.error('Failed to update cart:', error);
            this.showError('Failed to update cart. Please try again.');
        }
    }
    
    async updateCartDeliveryCharge() {
        try {
            const response = await fetch('/api/method/sa7ba_custom.api.update_cart_delivery', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Frappe-CSRF-Token': frappe.csrf_token
                },
                body: JSON.stringify({
                    area_code: this.selectedArea,
                    delivery_charge: this.deliveryCharge
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Refresh cart totals
                this.refreshCartDisplay();
            } else {
                this.showError(result.error || 'Failed to update cart');
            }
        } catch (error) {
            console.error('Failed to update cart:', error);
            this.showError('Failed to update cart. Please try again.');
        }
    }
    
    async removeDeliveryCharge() {
        try {
            const response = await fetch('/api/method/sa7ba_custom.api.remove_delivery_charge', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Frappe-CSRF-Token': frappe.csrf_token
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.refreshCartDisplay();
                sessionStorage.removeItem('selected_delivery_area');
            }
        } catch (error) {
            console.error('Failed to remove delivery charge:', error);
        }
    }
    
    refreshCartDisplay() {
        // This would call Webshop's cart refresh
        // Implementation depends on how Webshop handles cart updates
        if (window.updateCartTotals) {
            window.updateCartTotals();
        } else if (typeof frappe !== 'undefined' && frappe.cart) {
            frappe.cart.update();
        } else {
            // Fallback: reload page
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }
    }
    
    restoreSelectedArea() {
        const savedArea = sessionStorage.getItem('selected_delivery_area');
        if (savedArea) {
            setTimeout(() => {
                const select = document.getElementById('delivery-area-select');
                if (select) {
                    select.value = savedArea;
                    select.dispatchEvent(new Event('change'));
                }
            }, 500);
        }
    }
    
    showError(message) {
        // Show error message to user
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger alert-dismissible fade show';
        errorDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.delivery-area-section');
        if (container) {
            container.insertBefore(errorDiv, container.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
        }
    }
    
    // Guest checkout specific methods
    async processGuestCheckout(guestInfo) {
        try {
            const response = await fetch('/api/method/sa7ba_custom.api.process_guest_checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Frappe-CSRF-Token': frappe.csrf_token
                },
                body: JSON.stringify({
                    cart_data: {}, // Current cart data
                    guest_info: guestInfo
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                return result;
            } else {
                throw new Error(result.error || 'Guest checkout failed');
            }
        } catch (error) {
            console.error('Guest checkout failed:', error);
            throw error;
        }
    }
    
    validateGuestForm() {
        const form = document.getElementById('guest-checkout-form');
        if (!form) return false;
        
        const email = form.querySelector('#guest_email').value;
        const phone = form.querySelector('#guest_phone').value;
        const firstName = form.querySelector('#guest_first_name').value;
        
        const errors = [];
        
        if (!email) errors.push('Email is required');
        if (!phone) errors.push('Phone is required');
        if (!firstName) errors.push('First name is required');
        
        if (errors.length > 0) {
            this.showError(errors.join('<br>'));
            return false;
        }
        
        return true;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    window.deliveryAreaManager = new DeliveryAreaManager();
    window.deliveryAreaManager.init();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DeliveryAreaManager;
}
