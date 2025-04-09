$(window).on('load', function() {
    // Handle login page background - check if we're on the login page
    if (window.location.pathname === "/login" || 
        document.querySelector("body[data-route='login']") || 
        document.querySelector(".for-login")) {
        
        // Fetch the whitelabel settings for login page
        $.ajax({
            url: '/api/method/whitelabel.api.get_whitelabel_settings_for_login',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data.message && data.message.background_image) {
                    var bgImageUrl = data.message.background_image;
                    
                    // Make sure we have an absolute URL by prepending the site URL if needed
                    if (bgImageUrl.startsWith('/')) {
                        bgImageUrl = window.location.origin + bgImageUrl;
                    }
                    
                    console.log("Setting background image to:", bgImageUrl);
                    
                    // Apply the custom background with !important to override any existing styles
                    $("body").attr('style', 
                        "background: url('" + bgImageUrl + "') no-repeat center center fixed !important; " +
                        "background-size: cover !important"
                    );
                }
            },
            error: function(xhr, status, error) {
                console.error("Failed to fetch whitelabel settings:", error);
            }
        });
    }
    
    // Existing functionality for logged-in pages
    frappe.after_ajax(function () {
        if (frappe.boot.whitelabel_setting.show_help_menu) {
            // $('.dropdown-help').css('display','block');
            $('.dropdown-help').attr('style', 'display: block !important');
        }
        if (frappe.boot.whitelabel_setting.logo_width) {
            $('.app-logo').css('width',frappe.boot.whitelabel_setting.logo_width+'px');
        }
        if (frappe.boot.whitelabel_setting.logo_height) {
            $('.app-logo').css('height',frappe.boot.whitelabel_setting.logo_height+'px');
        }
        if (frappe.boot.whitelabel_setting.navbar_background_color) {
            $('.navbar').css('background-color',frappe.boot.whitelabel_setting.navbar_background_color)
        }
        if (frappe.boot.whitelabel_setting.custom_navbar_title_style && frappe.boot.whitelabel_setting.custom_navbar_title) {
            $(`<span style=${frappe.boot.whitelabel_setting.custom_navbar_title_style.replace('\n','')} class="hidden-xs hidden-sm">${frappe.boot.whitelabel_setting.custom_navbar_title}</span>`).insertAfter("#navbar-breadcrumbs")
        }
    })
})