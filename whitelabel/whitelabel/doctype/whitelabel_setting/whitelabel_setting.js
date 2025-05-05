//Working!
frappe.ui.form.on('Whitelabel Setting', {
    after_save: function(frm) {
        // Call our API endpoint to update the background image
        frappe.call({
            method: "whitelabel.api.update_login_background",
            callback: function(r) {
                // Always clear cache
                frappe.ui.toolbar.clear_cache();
                
                if (r.message && r.message.success) {
                    frappe.show_alert({
                        message: __("Login background updated successfully"),
                        indicator: 'green'
                    });
                } else if (r.message) {
                    frappe.show_alert({
                        message: __("Failed to update login background: " + r.message.message),
                        indicator: 'red'
                    });
                }
            }
        });
    }
});