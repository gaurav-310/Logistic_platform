from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from django.contrib.auth.models import User
from .models import Booking, VehicleType
from accounts.models import DriverProfile
import json
from django.http import JsonResponse
from django.conf import settings

# Booking detail view
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    goo = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'bookings/booking_detail.html', {'booking': booking,'goo':goo})

# Driver dashboard view to see all pending bookings
@login_required
def driver_dashboard(request):
    # Fetch all bookings with a pending status
    pending_bookings = Booking.objects.filter(status='pending').exclude(driver__isnull=False)

    context = {
        'pending_bookings': pending_bookings,
        
    }
    goo = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'accounts/driver_dashboard.html', context,{'goo':goo})

# Accept booking view
# bookings/views.py

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction

@login_required
def accept_booking(request, booking_id):
    # if not request.user.groups.filter(name='Drivers').exists():
    #     messages.error(request, "Only drivers can accept bookings.")
    #     return redirect('accounts:driver_dashboard')

    try:
        with transaction.atomic():
            # Lock the booking row to prevent race conditions
            booking = Booking.objects.select_for_update().get(id=booking_id)

            if booking.status != 'pending':
                messages.error(request, "This booking has already been accepted or is no longer available.")
                return redirect('accounts:driver_dashboard')

            # Assign the current driver to the booking and update status to 'accepted'
            booking.driver = request.user
            booking.status = 'accepted'
            booking.save()

        messages.success(request, "You have accepted the booking.")
    except Booking.DoesNotExist:
        messages.error(request, "Booking does not exist.")
    except Exception as e:
        messages.error(request, "An error occurred while accepting the booking.")
        print(f"Error in accept_booking view: {e}")

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
    # print(settings.GOOGLE_MAPS_API_KEY)
    vehicle_types = VehicleType.objects.all()
    goo = settings.GOOGLE_MAPS_API_KEY

    return render(request, 'bookings/booking_form.html', {'form': form, 'vehicle_types': vehicle_types,'goo':goo})

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
            status='pending'
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
    goo = settings.GOOGLE_MAPS_API_KEY
   
    return render(request, 'accounts/user_dashboard.html', {'bookings': bookings},{'goo': goo})

# Delete booking view
@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Booking deleted successfully.")
    return redirect('accounts:user_dashboard')


@login_required

def update_job_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, driver=request.user)

    if request.method == 'POST':
        job_status = request.POST.get('job_status')

        if job_status in dict(Booking.STATUS_CHOICES):
            booking.status = job_status
            booking.save()
            messages.success(request, 'Job status updated successfully.')
        else:
            messages.error(request, 'Invalid job status.')

    return redirect('accounts:driver_dashboard')

@login_required

def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, driver=request.user)

    if request.method == 'POST':
        booking.status = 'completed'
        booking.save()
        messages.success(request, 'Booking marked as completed.')

    

    return redirect('accounts:driver_dashboard')