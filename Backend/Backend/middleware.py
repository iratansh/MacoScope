# middleware.py

from django.utils.deprecation import MiddlewareMixin

class SessionDebugMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(f"Session Key on request: {request.session.session_key}")
        print(f"Session Data: {request.session.items()}")

    def process_response(self, request, response):
        print(f"Session Key on response: {request.session.session_key}")
        return response
