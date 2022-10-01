def handler404(request, *args, **kwargs):
    return render(request, "errors/404.html") 

handler404 = handler404