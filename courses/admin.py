from django.contrib import admin
from .models import Category, Course, Topic, AcademicYear


admin.site.register(Category) 
admin.site.register(AcademicYear)
admin.site.register(Course)
admin.site.register(Topic)