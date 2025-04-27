# decorators.py
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not request.user.is_authenticated:
                return redirect('login')  # Redirige al usuario a la página de inicio de sesión

            # Obtener el rol del usuario
            user_role = getattr(request.user, 'rol', None)

            # Verificar si el rol del usuario está en la lista de roles permitidos
            if user_role not in allowed_roles:
                return redirect('access_denied')  # Redirige a una página de acceso denegado

            # Si el usuario tiene un rol permitido, ejecutar la vista
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def cliente_required(view_func):
    return role_required(['Cliente'])(view_func)

def tecnico_required(view_func):
    return role_required(['Técnico'])(view_func)

def gestor_required(view_func):
    return role_required(['Gestor de Tareas'])(view_func)

def admin_required(view_func):
    return role_required(['Administrador'])(view_func)

def combined_role_required(*roles):
    allowed_roles = list(roles)
    return role_required(allowed_roles)