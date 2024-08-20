from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME

def dynamic_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                login_url = reverse('core_app:login')
                return redirect(f'{login_url}?{redirect_field_name}={request.get_full_path()}')
            elif request.user.is_authenticated and not request.user.is_coordinator:
                login_url = reverse('core_app:login')
                return redirect(f'{login_url}?{redirect_field_name}={request.get_full_path()}')
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
