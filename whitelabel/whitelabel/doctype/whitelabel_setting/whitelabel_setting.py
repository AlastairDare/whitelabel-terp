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
				# Log for debugging - all to Error Log List in UI
				frappe.log_error(f"Background image path: {self.background_image}", "Whitelabel Debug")
				
				# Get the source file path
				source_path = os.path.join(get_files_path(), os.path.basename(self.background_image))
				
				# Log source path for debugging
				frappe.log_error(f"Source path: {source_path}", "Whitelabel Debug")
				frappe.log_error(f"Source exists: {os.path.exists(source_path)}", "Whitelabel Debug")
				
				# Create the destination directory if it doesn't exist
				assets_dir = os.path.join(frappe.utils.get_bench_path(), 'sites', frappe.utils.get_site_path(), 'public', 'assets', 'whitelabel', 'images')
				
				# Log destination directory
				frappe.log_error(f"Destination directory: {assets_dir}", "Whitelabel Debug")
				frappe.log_error(f"Destination exists: {os.path.exists(assets_dir)}", "Whitelabel Debug")
				
				# Create directory if needed
				os.makedirs(assets_dir, exist_ok=True)
				
				# Set destination path with fixed filename
				dest_path = os.path.join(assets_dir, 'login-background.PNG')
				
				# Log destination path
				frappe.log_error(f"Destination path: {dest_path}", "Whitelabel Debug")
				
				# Try to copy the file
				shutil.copy2(source_path, dest_path)
				
				# Verify copy succeeded
				frappe.log_error(f"Copy succeeded: {os.path.exists(dest_path)}", "Whitelabel Debug")
				
				# If successful, try to log file permissions
				if os.path.exists(dest_path):
					import stat
					try:
						file_stat = os.stat(dest_path)
						permissions = stat.filemode(file_stat.st_mode)
						frappe.log_error(f"File permissions: {permissions}", "Whitelabel Debug")
						frappe.log_error(f"File size: {file_stat.st_size} bytes", "Whitelabel Debug")
					except Exception as stat_err:
						frappe.log_error(f"Could not get file stats: {str(stat_err)}", "Whitelabel Debug")
				
				frappe.db.commit()
				return True
			except Exception as e:
				frappe.log_error(f"Failed to copy background image: {str(e)}", "Whitelabel Background Update")
				return False
		return False


		
