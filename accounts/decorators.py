# accounts/decorators.py

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You are not authorized to view this page.")
        return _wrapped_view
    return decorator

