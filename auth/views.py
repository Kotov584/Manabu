from django.shortcuts import render

def login(request):
    return render(request, "auth/login.html")

def register(request):
    return render(request, "auth/register.html")

def locked(request):
    return render(request, "auth/locked.html")

def forgot_password(request):
    return render(request, "auth/forgot_password.html")