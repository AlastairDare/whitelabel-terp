# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def get_app_logo():
    import frappe
    if frappe.conf and frappe.conf.get("app_logo_url"):
        return frappe.conf.get("app_logo_url") or '/assets/whitelabel/images/whitelabel_logo.jpg'
    else:
        return '/assets/whitelabel/images/whitelabel_logo.jpg'