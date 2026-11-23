from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def role_required(*allowed_roles):
    """Require login and one of the listed roles for a dashboard view."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_superuser and "SYSTEM_ADMIN" in allowed_roles:
                return view_func(request, *args, **kwargs)
            if user.role not in allowed_roles:
                raise PermissionDenied("You do not have permission to access this dashboard.")
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
