

from django.db import models
from django.db import models
from django.contrib.auth.models import User



class VehicleType(models.Model):
    name = models.CharField(max_length=50)
    base_fare = models.DecimalField(max_digits=6, decimal_places=2)
    cost_per_km = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
# bookings/models.py



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
