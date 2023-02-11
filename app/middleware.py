from django.http import JsonResponse

class JSONContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'PUT'] and request.content_type != 'application/json':
            return JsonResponse({'error': 'Invalid Content-Type. Only JSON format is accepted.'}, status=400)
        return self.get_response(request)