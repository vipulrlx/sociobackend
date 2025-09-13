from django.contrib import admin
from .user import *
from .role import *
from .employee import *
from .menu import *
from .student import *
from .permission import *

# Customize Django Admin Site
admin.site.site_header = "Skill Next Admin"
admin.site.site_title = "Skill Next Admin"
admin.site.index_title = "Welcome to Skill Next Administration"
