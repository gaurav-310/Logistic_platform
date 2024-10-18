# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import UserRegistrationForm, DriverProfileForm
from .models import DriverProfile
from bookings.models import Booking  # Import Booking model from bookings app
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import role_required


# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            role = user.profile.role
            messages.success(request, "Registration successful.")
            # Redirect based on role
            if role == 'user':
                return redirect('accounts:user_dashboard')
            elif role == 'driver':
                return redirect('accounts:driver_dashboard')
            else:
                return redirect('accounts:admin_dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            role = user.profile.role
            messages.success(request, "Login successful.")
            # Redirect based on role
            if role == 'user':
                return redirect('accounts:user_dashboard')
            elif role == 'driver':
                return redirect('accounts:driver_dashboard')
            else:
                return redirect('accounts:admin_dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

# User dashboard - showing user's bookings
@login_required
@role_required(allowed_roles=['user'])
def user_dashboard(request):
    # Fetch all bookings for the logged-in user from the bookings app
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/user_dashboard.html', {'bookings': bookings})

# Driver dashboard - showing pending bookings to accept/reject
@login_required
@role_required(allowed_roles=['driver'])
@login_required
@role_required(allowed_roles=['driver'])
def driver_dashboard(request):
    # Fetch the driver profile
    driver = DriverProfile.objects.get(user=request.user)
    
    # Get all pending bookings (or add any filtering you need)
    pending_bookings = Booking.objects.filter(status='pending')
    
    context = {
        'driver_profile': driver,
        'pending_bookings': pending_bookings
    }
    
    return render(request, 'accounts/driver_dashboard.html', context)

# Admin dashboard
@login_required
@role_required(allowed_roles=['admin'])
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

# Confirm booking - User confirms a booking and drivers are notified
@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'pending'
    booking.save()
    
    # Notify all drivers (this will display in their dashboard)
    # Optionally implement email notifications here if needed
    
    messages.success(request, "Your booking has been confirmed and is awaiting driver approval.")
    return redirect('accounts:user_dashboard')
