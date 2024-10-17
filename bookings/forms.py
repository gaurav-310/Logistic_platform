# bookings/forms.py

from django import forms
from .models import Booking, VehicleType

# bookings/forms.py

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pickup_location', 'dropoff_location', 'vehicle_type']
        widgets ={
            'distance': forms.HiddenInput(),
            'estimated_cost': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        vehicle_choices = []
        for vehicle in VehicleType.objects.all():
            vehicle_choices.append(
                (vehicle.id, vehicle.name)
            )
        self.fields['vehicle_type'].choices = vehicle_choices

