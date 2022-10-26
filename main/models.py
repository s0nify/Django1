from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Services(models.Model):
    service_url = models.TextField()
    service_login = models.CharField(max_length=30)
    service_password = models.CharField(max_length=30)
    is_service_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.service_url

class PhoneManager(models.Model):
    phone_enable = models.BooleanField(default=True)

    def __bool__(self):
        return self.phone_enable