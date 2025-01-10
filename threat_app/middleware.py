import json
import requests
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from user_agents import parse
from .ai_model import detect_threat  # Use your AI model for threat detection
from .forms import LoginForm
from .models import RequestRecord

class BlockThreatMiddleware:
    """
    Middleware to check all requests for potential threats
    and block them before reaching the views.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process and validate the incoming request
        if self.is_threat(request):
            return HttpResponseForbidden("Threat detected! Request has been blocked.")

        # Continue processing the request
        response = self.get_response(request)
        return response

    def is_threat(self, request):
        """
        Analyze request data for threats:
        - Payload (POST data)
        - Query parameters
        - Headers
        """
        # Combine request data for threat detection
        request_payload = {
            "POST": str(request.POST),  # POST payload
            "GET": str(request.GET),  # Query parameters
            "BODY": request.body.decode("utf-8", errors="ignore") if request.body else "",  # Raw body payload
            "HEADERS": str(request.headers)  # Headers
        }

        # Check for threats using the AI model
        combined_payload = json.dumps(request_payload)  # Combine as a single string
        is_threat = detect_threat(combined_payload)  # Analyze with your AI model
        request_data = combined_payload
        ip_address = self.get_client_ip(request)

        # User-agent parsing
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        parsed_user_agent = parse(user_agent)
        device_name = f"{parsed_user_agent.device.family} - {parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"

        # Fetch location and ISP
        location, isp, postel, timezone = self.get_ip_info(ip_address)
        # Handle valid login attempts for POST requests
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return False
        # If a threat is detected, log it and block the request
        if is_threat:
            self.log_threat(ip_address, device_name, user_agent, location, isp, combined_payload)
            self.send_admin_alert(ip_address, location, isp, user_agent, request_data, device_name, postel, timezone)
            return True
        return False

    def log_threat(self, ip, device_name, browser, location, isp, payload):
        """Log the threat details in the database."""
        RequestRecord.objects.create(
            ip_address=ip,
            device_name=device_name,
            browser=browser,
            location=location,
            isp=isp,
            threat_detected=True
        )
        print(f"Threat logged: IP={ip}, Payload={payload[:200]}")  # Print for debugging

    def send_admin_alert(self, ip, location, isp, user_agent, payload, device_name, postel, timezone):
        """Send an email alert to the admin for detected threats."""
        subject = "Threat Alert: Suspicious Request Detected!"
        message = f"""
        A threat has been detected:
        IP Address: {ip}
        Device Name: {device_name}
        Browser Info: {user_agent}
        Location: {location}
        ISP: {isp}
        Postel: {postel}
        Timezone: {timezone}
        Payload: {payload}
        """
        send_mail(subject, message, 'hadiraza1109@gmail.com', ['mominalikhoker589@gmial.com', 'nadir722457@gmail.com'])

    def get_client_ip(self, request):
        """Get the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # Actual client IP
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip

    def get_ip_info(self, ip):
        """Fetch IP-related information like location, ISP, etc."""
        try:
            token = "b730135212ef34"
            response = requests.get(f'https://ipinfo.io/{ip}?token={token}')
            data = response.json()
            location = data.get('city', 'Unknown') + ", " + data.get('region', 'Unknown') + ", " + data.get('country', 'Unknown')
            postel = data.get('postal', 'Unknown')
            timezone = data.get('timezone', 'Unknown')
            isp = data.get('org', 'Unknown ISP')
            return location, isp, postel, timezone
        except Exception as e:
            print(f"Error fetching IP info: {e}")
            return "Unknown", "Unknown ISP", "Unknown", "Unknown"
