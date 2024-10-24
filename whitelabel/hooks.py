# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
from . import __logo__ as app_logo


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


website_context = {
	"favicon": app_logo or "/assets/whitelabel/images/whitelabel_logo.svg",
	"splash_image": app_logo or "/assets/whitelabel/images/whitelabel_logo.svg"
}
after_migrate = ['whitelabel.api.whitelabel_patch']

boot_session = "whitelabel.api.boot_session"

fixtures = [
    {"dt": "Custom Field", "filters": [["Translation","source_text","like","%ERPNext%"]]}
]

