# app/middleware.py
from django.utils.deprecation import MiddlewareMixin

class BypassHostValidationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Замінюємо HTTP_HOST на дозволений хост
        request.META['HTTP_HOST'] = 'localhost'
        return self.get_response(request)