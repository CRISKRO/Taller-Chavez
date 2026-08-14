from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def role_required(allowed_roles=None):
    """
    Decorador que restringe el acceso a las vistas según el rol del usuario.
    Si el usuario no está autenticado, redirige al login.
    Si el rol del usuario no está en allowed_roles, dispara PermissionDenied (HTTP 403 Forbidden).
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.is_superuser or request.user.rol in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("No tienes permisos suficientes para acceder a este módulo.")
        return _wrapped_view
    return decorator

def admin_required(view_func):
    return role_required(['ADMIN'])(view_func)

def recepcionista_required(view_func):
    return role_required(['ADMIN', 'RECEPCIONISTA'])(view_func)

def mecanico_required(view_func):
    return role_required(['ADMIN', 'MECANICO'])(view_func)
