# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "whitelabel"
app_title = "Whitelabel"
app_publisher = "Bhavesh Maheshwari"
app_description = "ERPNext Whitelabel"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "maheshwaribhavesh95863@gmail.com"
app_license = "MIT"
app_logo_url = '/assets/whitelabel/images/whitelabel_logo.jpg'

app_include_css = "/assets/whitelabel/css/whitelabel_app.css"
app_include_js = "/assets/whitelabel/js/whitelabel.js"

web_include_css = "/assets/whitelabel/css/whitelabel_web.css"

# Update this to use a function instead of directly accessing app_logo
def get_website_context(context):
    # This is only executed when Frappe is fully initialized
    try:
        import frappe
        custom_logo = None
        
        # Try to get logo from Website Settings
        if frappe.db.exists("Website Settings", "Website Settings"):
            settings = frappe.get_doc("Website Settings", "Website Settings")
            if settings.app_logo:
                custom_logo = settings.app_logo
        
        # Try to get from Whitelabel Settings (if you have such a doctype)
        elif frappe.db.exists("Whitelabel Setting", "Whitelabel Setting"):
            settings = frappe.get_doc("Whitelabel Setting", "Whitelabel Setting")
            if hasattr(settings, 'app_logo') and settings.app_logo:
                custom_logo = settings.app_logo
        
        # Use custom logo if found, otherwise fallback to default
        logo_path = custom_logo or "/assets/whitelabel/images/whitelabel_logo.svg"
        
        return {
            "favicon": logo_path,
            "splash_image": logo_path
        }
    except Exception:
        # Fallback to default if any error occurs
        return {
            "favicon": "/assets/whitelabel/images/whitelabel_logo.svg",
            "splash_image": "/assets/whitelabel/images/whitelabel_logo.svg"
        }

website_context = get_website_context

after_migrate = ['whitelabel.api.whitelabel_patch']

boot_session = "whitelabel.api.boot_session"

fixtures = [
    {"dt": "Custom Field", "filters": [["Translation","source_text","like","%ERPNext%"]]},
    {"dt": "Website Settings", "filters": [["name", "=", "Website Settings"]]}
]