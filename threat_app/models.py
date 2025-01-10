from django.db import models

from django.contrib.auth.models import AbstractUser

class RequestRecord(models.Model):
    ip_address = models.GenericIPAddressField()
    device_name = models.CharField(max_length=255)
    browser = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    isp = models.CharField(max_length=255)
    threat_detected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
