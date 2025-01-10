from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_model.threat_detector import ThreatDetector


class ThreatDetectionAPI(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.threat_detector = ThreatDetector()

    def post(self, request):
        # Extract data from the request body
        data = request.data.get("features", None)

        # Check for missing or empty data
        if data is None or not data.strip():
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check for threats
            if self.threat_detector.is_threat(data):
                return Response(
                    {"message": "Threat detected", "status": "blocked"},
                    status=status.HTTP_403_FORBIDDEN
                )
            else:
                return Response({"message": "No threat detected", "status": "allowed"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # GET method is not allowed for this endpoint
        return Response({"detail": "Method 'GET' not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
