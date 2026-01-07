frappe.ui.form.on('Delivery Area', {
    refresh: function(frm) {
        // Add custom buttons
        frm.add_custom_button(__('View Orders'), function() {
            frappe.set_route('List', 'Sales Order', {
                'shipping_address.custom_delivery_area': frm.doc.name
            });
        });
        
        frm.add_custom_button(__('Get Revenue'), function() {
            frappe.call({
                method: 'sa7ba_custom.doctype.delivery_area.delivery_area.get_total_revenue',
                args: {
                    docname: frm.doc.name
                },
                callback: function(r) {
                    if(r.message) {
                        frappe.msgprint({
                            title: 'Total Revenue',
                            message: 'KWD ' + r.message.toFixed(3),
                            indicator: 'green'
                        });
                    }
                }
            });
        });
        
        // Set default estimated time if empty
        if (!frm.doc.estimated_delivery_time) {
            frm.set_value('estimated_delivery_time', '2-3 hours');
        }
    },
    
    validate: function(frm) {
        // Ensure delivery charge is positive
        if (frm.doc.delivery_charge <= 0) {
            frappe.msgprint(__('Delivery charge must be greater than 0'));
            frappe.validated = false;
        }
        
        // Validate area code format
        if (frm.doc.area_code && !/^[A-Z]{3,6}$/.test(frm.doc.area_code)) {
            frappe.msgprint(__('Area code should be 3-6 uppercase letters'));
            frappe.validated = false;
        }
    },
    
    area_code: function(frm) {
        // Auto-format area code to uppercase
        if (frm.doc.area_code) {
            frm.set_value('area_code', frm.doc.area_code.toUpperCase());
        }
    },
    
    delivery_charge: function(frm) {
        // Show warning if delivery charge is too high
        if (frm.doc.delivery_charge > 10) {
            frappe.msgprint({
                title: 'High Delivery Charge',
                message: 'This delivery charge is quite high. Please confirm it\'s correct.',
                indicator: 'orange'
            });
        }
    }
});
