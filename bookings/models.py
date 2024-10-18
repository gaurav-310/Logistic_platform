# bookings/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class VehicleType(models.Model):
    name = models.CharField(max_length=50)
    base_fare = models.DecimalField(max_digits=6, decimal_places=2)
    cost_per_km = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.user.username}'s Booking ({self.pickup_location} to {self.dropoff_location})"