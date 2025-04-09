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
				
				# Get the app path for whitelabel
				try:
					# Use frappe's get_app_path function
					app_path = frappe.get_app_path('whitelabel')
					frappe.log_error(f"App path: {app_path}", "Whitelabel Debug")
				except Exception as app_err:
					frappe.log_error(f"Could not get app path: {str(app_err)}", "Whitelabel Debug")
					# Fallback: try to detect manually using bench path
					bench_path = frappe.utils.get_bench_path()
					app_path = os.path.join(bench_path, 'apps', 'whitelabel')
					frappe.log_error(f"Fallback app path: {app_path}", "Whitelabel Debug")
				
				# Create the destination directory in the app's public folder
				public_path = os.path.join(app_path, 'public', 'images')
				os.makedirs(public_path, exist_ok=True)
				frappe.log_error(f"Public path: {public_path}", "Whitelabel Debug")
				
				# Set destination path with fixed filename
				dest_path = os.path.join(public_path, 'login-background.PNG')
				
				# Delete existing file if it exists
				if os.path.exists(dest_path):
					os.remove(dest_path)
					frappe.log_error(f"Deleted existing file at {dest_path}", "Whitelabel Debug")
				
				# Copy the file
				shutil.copy2(source_path, dest_path)
				frappe.log_error(f"Copied file to {dest_path}", "Whitelabel Debug")
				
				# Verify copy succeeded
				if not os.path.exists(dest_path):
					frappe.log_error("Copy failed: Destination file doesn't exist", "Whitelabel Error")
					return False
				
				# Create a timestamp for cache busting
				import time
				timestamp = int(time.time())
				
				frappe.log_error(f"Image should be accessible via: /assets/whitelabel/images/login-background.PNG?v={timestamp}", "Whitelabel Debug")
				
				frappe.db.commit()
				return {"success": True, "timestamp": timestamp}
			except Exception as e:
				frappe.log_error(f"Failed to copy background image: {str(e)}", "Whitelabel Error")
				return False
		return False