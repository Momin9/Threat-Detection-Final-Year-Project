import os
import unittest
import json

import django
from django.test import Client
from rest_framework import status

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "threat_detection_app.settings")
django.setup()
class ThreatDetectionAPITestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        self.url = "/api/threat-detection/"

    def test_valid_non_threat_data(self):
        """Test valid non-threat data"""
        data = {"features": "0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0"}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("No threat detected", response.json().get("message"))

    def test_valid_threat_data(self):
        """Test valid threat data"""
        data = {"features": "1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0"}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Threat detected", response.json().get("message"))

    def test_invalid_data_format(self):
        """Test invalid data format (non-numeric values)"""
        data = {"features": "invalid,data"}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid input format", response.json().get("error"))

    def test_no_features_key(self):
        """Test missing 'features' key"""
        data = {}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No data provided", response.json().get("error"))

    def test_empty_features_value(self):
        """Test empty 'features' value"""
        data = {"features": ""}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No data provided", response.json().get("error"))

    def test_partial_features_data(self):
        """Test insufficient number of features"""
        data = {"features": "0.1,0.2,0.3"}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid input format", response.json().get("error"))

    def test_get_request(self):
        """Test GET request to the endpoint"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn("Method 'GET' not allowed", response.json().get("detail"))

    def test_boundary_values(self):
        """Test boundary values for features"""
        data = {"features": "0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0"}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("No threat detected", response.json().get("message"))

        data = {"features": "1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0"}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Threat detected", response.json().get("message"))
