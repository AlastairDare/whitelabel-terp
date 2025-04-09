# -*- coding: utf-8 -*-
# Copyright (c) 2021, Bhavesh Maheshwari and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.installer import update_site_config
import os
import shutil
from frappe.utils import get_files_path

class WhitelabelSetting(Document):
	def validate(self):
		system_settings_doc = frappe.get_doc("System Settings","System Settings")
		navbar_settings_doc = frappe.get_doc("Navbar Settings","Navbar Settings")
		website_doc = frappe.get_doc("Website Settings","Website Settings")
		self.set_app_name(system_settings_doc)
		self.set_theme_attr(navbar_settings_doc,website_doc)
		self.disable_onboarding(system_settings_doc)
		self.set_log_notification(system_settings_doc)
		self.set_footer(system_settings_doc)
		system_settings_doc.save(ignore_permissions = True)
		navbar_settings_doc.save(ignore_permissions = True)
		website_doc.save(ignore_permissions = True)

	def set_app_name(self,system_settings_doc):	
		if self.whitelabel_app_name:
			system_settings_doc.app_name = self.whitelabel_app_name
		else:
			if "erpnext" in frappe.get_installed_apps():
				system_settings_doc.app_name = "ERPNext"
			else:
				system_settings_doc.app_name = "Frappe"

	def set_theme_attr(self,navbar_settings_doc,website_doc):
		if self.application_logo:
			navbar_settings_doc.app_logo = self.application_logo
			website_doc.app_logo = self.application_logo
			website_doc.splash_image = self.application_logo
			update_site_config("app_logo_url",self.application_logo)
			frappe.clear_cache()
		else:
			navbar_settings_doc.app_logo = ""
			website_doc.app_logo = ""
			website_doc.splash_image = ""
			update_site_config("app_logo_url",False)
			frappe.clear_cache()
	
	def disable_onboarding(self,system_settings_doc):
		if self.ignore_onboard_whitelabel == 1:
			system_settings_doc.enable_onboarding = 0
		else:
			system_settings_doc.enable_onboarding = 1
	
	def set_log_notification(self,system_settings_doc):
		system_settings_doc.disable_system_update_notification = self.disable_new_update_popup
		system_settings_doc.disable_change_log_notification = self.disable_new_update_popup

	def set_footer(self,system_settings_doc):
		system_settings_doc.email_footer_address = self.email_footer_address
		system_settings_doc.disable_standard_email_footer = self.disable_standard_footer
		system_settings_doc.hide_footer_in_auto_email_reports = self.disable_standard_footer
	
	def copy_background_to_assets(self):
		"""Copy the background image to assets folder whenever whitelabel settings is saved"""
		if self.background_image:
			try:
				# Get the source file path
				source_path = os.path.join(get_files_path(), os.path.basename(self.background_image))
				frappe.log_error(f"Source path: {source_path}", "Whitelabel Debug")
				
				if not os.path.exists(source_path):
					frappe.log_error(f"Source file does not exist: {source_path}", "Whitelabel Error")
					return False
				
				# Create the destination directory if it doesn't exist
				assets_dir = os.path.join(frappe.utils.get_bench_path(), 'sites', frappe.utils.get_site_path(), 'public', 'assets', 'whitelabel', 'images')
				os.makedirs(assets_dir, exist_ok=True)
				
				# Find an available incremental filename
				suffix = 1
				while True:
					test_path = os.path.join(assets_dir, f'login-background-{suffix}.PNG')
					if not os.path.exists(test_path):
						break
					suffix += 1
					
				# Create a new incremental file
				incremental_path = os.path.join(assets_dir, f'login-background-{suffix}.PNG')
				
				# Copy to both the standard path and incremental path
				shutil.copy2(source_path, incremental_path)
				
				# Also update the standard path for normal operation
				standard_path = os.path.join(assets_dir, 'login-background.PNG')
				shutil.copy2(source_path, standard_path)
				
				frappe.log_error(f"Created incremental file: {incremental_path}", "Whitelabel Debug")
				frappe.log_error(f"Web accessible URL: /assets/whitelabel/images/login-background-{suffix}.PNG", "Whitelabel Debug")
				
				# Try to access the file via HTTP to verify
				import requests
				try:
					site_url = frappe.utils.get_url()
					test_url = f"{site_url}/assets/whitelabel/images/login-background-{suffix}.PNG"
					response = requests.head(test_url, timeout=5)
					frappe.log_error(f"HTTP Status for incremental file: {response.status_code}", "Whitelabel Debug")
				except Exception as req_err:
					frappe.log_error(f"Error checking incremental file: {str(req_err)}", "Whitelabel Debug")
				
				frappe.db.commit()
				return {"success": True, "suffix": suffix}
			except Exception as e:
				frappe.log_error(f"Failed to copy background image: {str(e)}", "Whitelabel Error")
				return False
		return False