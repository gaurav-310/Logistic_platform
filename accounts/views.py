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
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib import messages
from .models import Profile



# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user.save()
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
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Attempt to authenticate with username
            user = authenticate(request, username=username_or_email, password=password)
            
            if user is None:
                # Attempt to authenticate with email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                role = user.profile.role
                messages.success(request, "Login successful.")
                # Redirect based on role
                if role == 'admin':
                    return redirect('accounts:admin_dashboard')
                elif role == 'driver':
                    return redirect('accounts:driver_dashboard')
                else:
                    return redirect('accounts:user_dashboard')
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
# @login_required
# @role_required(allowed_roles=['driver'])
# def driver_dashboard(request):
#     # Fetch the driver profile
#     driver_profile, created = DriverProfile.objects.get_or_create(user=request.user)
    
#     # Get all pending bookings and accepted bookings
#     pending_bookings = Booking.objects.filter(status='pending')
#     accepted_bookings = Booking.objects.filter(status='accepted', driver=request.user)

#     if request.method == 'POST':
#         # Update the current location when the form is submitted
#         current_location = request.POST.get('current_location')
#         if current_location:
#             driver_profile.current_location = current_location
#             driver_profile.save()
#             messages.success(request, 'Location updated successfully.')
#             # Redirect to prevent form re-submission
#             return redirect('accounts:driver_dashboard')
    
#     context = {
#         'driver_profile': driver_profile,  # Make sure this contains current_location
#         'current_location': driver_profile.current_location,  # Pass the current location to the template
#         'pending_bookings': pending_bookings,
#         'accepted_bookings': accepted_bookings
#     }
    
#     return render(request, 'accounts/driver_dashboard.html', context)


@login_required
@role_required(allowed_roles=['driver'])
def driver_dashboard(request):
    driver_profile, created = DriverProfile.objects.get_or_create(user=request.user)
    
    pending_bookings = Booking.objects.filter(status='pending')
    active_bookings = Booking.objects.filter(driver=request.user).exclude(status='completed')
    completed_bookings = Booking.objects.filter(driver=request.user, status='completed')
    
    if request.method == 'POST':
        current_location = request.POST.get('current_location')
        if current_location:
            driver_profile.current_location = current_location
            driver_profile.save()
            messages.success(request, 'Location updated successfully.')
            return redirect('accounts:driver_dashboard')
    
    context = {
        'driver_profile': driver_profile,
        'current_location': driver_profile.current_location,
        'pending_bookings': pending_bookings,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
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

@login_required
def booking_detail_view(request, booking_id):
    # Get the booking object based on booking_id
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Fetch the driver assigned to the booking (if any)
    driver_profile = None
    if booking.driver:
        driver_profile = DriverProfile.objects.get(user=booking.driver)
    
    context = {
        'booking': booking,
        'driver_profile': driver_profile,  # Contains driver's current location
    }
    return render(request, 'accounts/booking_detail.html', context)

@login_required
@role_required(allowed_roles=['driver'])
def update_job_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, driver=request.user)

    if request.method == 'POST':
        job_status = request.POST.get('job_status')

        # Update the booking status based on the driver's selection
        if job_status == 'en_route_to_pickup':
            booking.status = 'en_route_to_pickup'
        elif job_status == 'goods_collected':
            booking.status = 'goods_collected'
        elif job_status == 'delivered':
            booking.status = 'delivered'

        booking.save()
        messages.success(request, 'Job status updated successfully.')
    
    return redirect('accounts:driver_dashboard')

@login_required
@role_required(allowed_roles=['driver'])
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, driver=request.user)

    if request.method == 'POST':
        booking.status = 'completed'
        booking.save()
        messages.success(request, 'Booking marked as completed.')
    
    return redirect('accounts:driver_dashboard')


def custom_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate with username
        user = authenticate(request, username=username_or_email, password=password)

        

        if user is not None:
            login(request, user)
            if user.is_staff:
                # Redirect staff/admin users to the admin dashboard
                return redirect('admin_dashboard:dashboard_home')
            else:
                # Redirect regular users to the user dashboard
                return redirect('accounts:user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'registration/login.html')
@login_required
@role_required(allowed_roles=['admin'])
def manage_users(request):
    users = User.objects.all()
    return render(request, 'accounts/manage_users.html', {'users': users})
@login_required
@role_required(allowed_roles=['admin'])
def view_all_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'accounts/view_all_bookings.html', {'bookings': bookings})
from django.db.models import Count, Avg, F, ExpressionWrapper, fields

@login_required
@role_required(allowed_roles=['admin'])
def analytics(request):
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    total_drivers = Profile.objects.filter(role='driver').count()

    # Calculate average trip duration
    average_trip_time = Booking.objects.filter(status='completed').annotate(
        trip_duration=ExpressionWrapper(
            F('end_time') - F('start_time'),
            output_field=fields.DurationField()
        )
    ).aggregate(average_duration=Avg('trip_duration'))['average_duration']

    # Driver performance
    driver_performance = Booking.objects.filter(status='completed').values('driver__username').annotate(
        trips_completed=Count('id'),
        average_trip_time=Avg(
            ExpressionWrapper(
                F('end_time') - F('start_time'),
                output_field=fields.DurationField()
            )
        )
    )

    context = {
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_drivers': total_drivers,
        'average_trip_time': average_trip_time,
        'driver_performance': driver_performance,
    }
    return render(request, 'accounts/analytics.html', context)
