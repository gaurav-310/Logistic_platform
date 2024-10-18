from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DriverProfile,Profile

from django import forms
from django.contrib.auth.models import User
from .models import Profile

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
            # No need to manually create the profile, signal will handle it
            user.profile.role = self.cleaned_data['role']
            user.profile.save()
        return user
class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['location', 'vehicle']