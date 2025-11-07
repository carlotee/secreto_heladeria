from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def rol_requerido(*roles_permitidos):
    """
    Decorador que valida si el usuario tiene los roles necesarios
    para acceder a las vistas del módulo de Proveedores.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # 🔐 Verificar autenticación
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')

            # Mapa de equivalencias
            rol_map = {
                'Administrador': 'admin',
                'Proveedor': 'proveedor',
                'Cliente': 'cliente',
            }

            roles_campo = [rol_map.get(r, r.lower()) for r in roles_permitidos]
            tiene_permiso = getattr(request.user, 'rol', None) in roles_campo

            # También verificar por grupos de Django
            if not tiene_permiso:
                tiene_permiso = request.user.groups.filter(name__in=roles_permitidos).exists()

            if not tiene_permiso:
                rol_display = getattr(request.user, 'get_rol_display', lambda: 'Desconocido')()
                messages.error(
                    request,
                    f'No tienes permisos para acceder a esta sección. '
                    f'Tu rol actual es: {rol_display}. '
                    f'Se requiere uno de estos roles: {", ".join(roles_permitidos)}.'
                )
                return redirect('prov_dashboard') 

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
