
# # accounts/views.py

# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from .forms import UserRegistrationForm
# from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from .decorators import role_required


# # accounts/views.py





# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             role = user.profile.role
#             messages.success(request, "Registration successful.")
#             # Redirect based on role
#             if role == 'user':
#                 return redirect('accounts:user_dashboard')
#             elif role == 'driver':
#                 return redirect('accounts:driver_dashboard')
#             else:
#                 return redirect('accounts:admin_dashboard')
#         else:
#             messages.error(request, "Registration failed. Please correct the errors.")
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             role = user.profile.role
#             messages.success(request, "Login successful.")
#             # Redirect based on role
#             if role == 'user':
#                 return redirect('accounts:user_dashboard')
#             elif role == 'driver':
#                 return redirect('accounts:driver_dashboard')
#             else:
#                 return redirect('accounts:admin_dashboard')
#         else:
#             messages.error(request, "Invalid credentials.")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form})



# def logout_view(request):
#     logout(request)
#     messages.info(request, "You have successfully logged out.")
#     return redirect('home')





# @login_required
# @role_required(allowed_roles=['user'])
# def user_dashboard(request):
#     return render(request, 'accounts/user_dashboard.html')



# @login_required
# @role_required(allowed_roles=['driver'])
# def driver_dashboard(request):
#     return render(request, 'accounts/driver_dashboard.html')


# @login_required
# @role_required(allowed_roles=['admin'])
# def admin_dashboard(request):
#     return render(request, 'accounts/admin_dashboard.html')

# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, DriverProfileForm
from .models import DriverProfile
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import role_required

# Registration view
# accounts/views.py

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set role in the user profile
            role = form.cleaned_data.get('role')
            user.profile.role = role
            user.profile.save()

            # If the role is driver, ensure DriverProfile is created
            if role == 'driver':
                DriverProfile.objects.create(user=user)

            login(request, user)
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

# User dashboard
@login_required
@role_required(allowed_roles=['user'])
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')

# Driver dashboard
@login_required
@role_required(allowed_roles=['driver'])
def driver_dashboard(request):
    driver_profile, created = DriverProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = DriverProfileForm(request.POST, instance=driver_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Information updated successfully.")
            return redirect('accounts:driver_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DriverProfileForm(instance=driver_profile)

    context = {
        'form': form,
        'driver_profile': driver_profile,
    }
    return render(request, 'accounts/driver_dashboard.html', context)

# Admin dashboard
@login_required
@role_required(allowed_roles=['admin'])
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')
