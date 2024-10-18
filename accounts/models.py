# accounts/models.py

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensures one-to-one relationship
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)
    vehicle = models.CharField(max_length=100, blank=True, null=True)
    current_location = models.CharField(max_length=255, null=True, blank=True)
    current_status = models.CharField(max_length=50, default='Available')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user.profile.role}"