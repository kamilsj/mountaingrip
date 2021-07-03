from apps.notifications.models import Notification
from func.notif import Notif


class MGMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.notif = {}
    
    def __call__(self, request):
        response = self.get_response(request)
        return response



