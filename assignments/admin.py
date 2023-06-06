from django.contrib import admin
from .models import Assignment, UserAssignment

admin.site.register(Assignment)
admin.site.register(UserAssignment)