from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from ai_model.threat_detector import ThreatDetector

class ThreatDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.detector = ThreatDetector()

    def __call__(self, request):
        try:
            # Example: Parse request body for features
            request_data = request.body.decode("utf-8")
            if self.detector.is_threat(request_data):
                send_mail(
                    'Threat Detected',
                    'A request was blocked due to a potential threat.',
                    settings.EMAIL_HOST_USER,
                    ['admin@example.com']
                )
                return HttpResponse("Forbidden: Threat detected", status=403)
        except Exception as e:
            print(f"Middleware error: {e}")
        return self.get_response(request)
