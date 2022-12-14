"""Manabu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path  
from django.shortcuts import render
from . import views, errors   

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', include('auth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('courses/', include('courses.urls')),
    path('grades/', include('grades.urls')),
    path('assessments/', include('assessments.urls')),
    path('exams/', include('exams.urls')),
    path('groups/', include('groups.urls')),
    path('contacts/', include('contacts.urls')),
    path('file-manager/', include('file_manager.urls')),
    path('messenger/', include('messenger.urls')),
    path('permissions/', include('permissions.urls')),
    path('roles/', include('roles.urls')),
    path('settings/', include('settings.urls')),
    path('transactions/', include('transactions.urls')), 
    path('users/', include('users.urls')) 
] 