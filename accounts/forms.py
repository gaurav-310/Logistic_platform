# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DriverProfile, Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('driver', 'Driver'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create Profile
            role = self.cleaned_data['role']
            profile = Profile.objects.create(user=user, role=role)
            profile.save()
            # If the role is 'driver', create DriverProfile
            if role == 'driver':
                DriverProfile.objects.create(user=user)
        return user

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['current_location']  # Include any other fields you have in DriverProfile
