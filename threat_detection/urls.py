from django.urls import path
from .views import ThreatDetectionAPI

urlpatterns = [
    path('api/threat-detection/', ThreatDetectionAPI.as_view(), name='threat_detection_api'),
]
