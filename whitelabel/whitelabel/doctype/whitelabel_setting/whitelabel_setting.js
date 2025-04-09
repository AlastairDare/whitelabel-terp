frappe.ui.form.on('Whitelabel Setting', {
    after_save: function(frm) {
        // First call our API endpoint to update the background image
        frappe.call({
            method: "whitelabel.api.update_login_background",
            callback: function(r) {
                // Always clear cache regardless of success or failure
                frappe.ui.toolbar.clear_cache();
                
                if (r.message && r.message.success) {
                    // Show success message with link to the incremental file
                    let suffix = r.message.suffix || '';
                    let fileUrl = '';
                    
                    if (suffix) {
                        fileUrl = `/assets/whitelabel/images/login-background-${suffix}.PNG`;
                        
                        frappe.show_alert({
                            message: __(`Login background updated successfully. <a href="${fileUrl}" target="_blank">View file</a>`),
                            indicator: 'green'
                        }, 15);
                        
                        // Also offer to open login page
                        setTimeout(function() {
                            frappe.confirm(
                                'Would you like to verify the login background?',
                                function() {
                                    // Open both the incremental file and login page
                                    window.open(fileUrl, '_blank');
                                    window.open('/login', '_blank');
                                },
                                function() {
                                    // No - just continue
                                }
                            );
                        }, 1000);
                    } else {
                        frappe.show_alert({
                            message: __("Login background updated successfully"),
                            indicator: 'green'
                        });
                    }
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