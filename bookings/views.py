from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from django.contrib.auth.models import User
from .models import Booking, VehicleType
from accounts.models import DriverProfile
import json
from django.http import JsonResponse
# Booking detail view
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

# Driver dashboard view to see all pending bookings
@login_required
def driver_dashboard(request):
    # Fetch all bookings with a pending status
    pending_bookings = Booking.objects.filter(status='pending').exclude(driver__isnull=False)

    context = {
        'pending_bookings': pending_bookings,
    }
    return render(request, 'accounts/driver_dashboard.html', context)

# Accept booking view
@login_required
def accept_booking(request, booking_id):
    # Fetch the booking with pending status
    booking = get_object_or_404(Booking, id=booking_id, status='pending')

    # If a driver has already accepted it, don't allow others to accept
    if booking.driver is not None:
        messages.error(request, "This booking has already been accepted by another driver.")
        return redirect('accounts:driver_dashboard')

    # Assign the current driver to the booking and update status to approved
    booking.driver = request.user
    booking.status = 'approved'
    booking.save()

    messages.success(request, "You have accepted the booking.")
    return redirect('accounts:driver_dashboard')

# Reject booking view
@login_required
def reject_booking(request, booking_id):
    # Fetch the booking with pending status
    booking = get_object_or_404(Booking, id=booking_id, status='pending')

    # Simply reject the booking
    booking.status = 'rejected'
    booking.save()

    messages.success(request, "You have rejected the booking.")
    return redirect('accounts:driver_dashboard')

# Create booking view
@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Booking created successfully.")
            
            # Redirect to the booking detail page, passing the booking id
            return redirect('bookings:booking_detail', pk=booking.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()
    
    vehicle_types = VehicleType.objects.all()
    return render(request, 'bookings/booking_form.html', {'form': form, 'vehicle_types': vehicle_types})

# Confirm booking view
@login_required
def confirm_booking(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pickup_location = data.get('pickup_location')
        dropoff_location = data.get('dropoff_location')
        vehicle_type_id = data.get('vehicle_type')
        date = data.get('date')
        estimated_cost = data.get('estimated_cost')

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            vehicle_type_id=vehicle_type_id,
            date=date,
            estimated_cost=estimated_cost,
            status='confirmed'
        )

        # Notify drivers about the new booking request
        drivers = DriverProfile.objects.all()
        for driver in drivers:
            # Implement your notification logic here
            pass

        return JsonResponse({'message': 'Booking confirmed successfully!'})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

# User dashboard view
@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/user_dashboard.html', {'bookings': bookings})

# Delete booking view
@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Booking deleted successfully.")
    return redirect('accounts:user_dashboard')
