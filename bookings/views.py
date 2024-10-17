from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from .models import Booking, VehicleType

@login_required
def create_booking(request):
    # If the request method is POST, we handle form submission
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                # Save the booking without committing to add the user
                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()  # Save the booking
                messages.success(request, "Booking created successfully.")
                return redirect('bookings:booking_detail', pk=booking.pk)
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'bookings/booking_form.html', {'form': form})
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # If the request method is GET, we display the booking form
        form = BookingForm()
    
    # Fetch vehicle types and pass them to the template
    vehicle_types = VehicleType.objects.all()
    
    return render(request, 'bookings/booking_form.html', {'form': form, 'vehicle_types': vehicle_types})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'bookings/booking_details.html', {'booking': booking})
