from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def rol_requerido_proveedor(*roles_permitidos):
    """
    Decorador que verifica si el usuario tiene uno de los roles permitidos
    para las vistas del módulo de Proveedores.
    
    Uso:
        @rol_requerido_proveedor('Proveedor', 'Administrador')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            rol_map = {
                'Administrador': 'admin',
                'Proveedor': 'proveedor',
                'Cliente': 'cliente',
            }

            roles_campo = [rol_map.get(r, r.lower()) for r in roles_permitidos]
            tiene_permiso = request.user.rol in roles_campo

            if not tiene_permiso:
                tiene_permiso = request.user.groups.filter(name__in=roles_permitidos).exists()

            if not tiene_permiso:
                messages.error(
                    request,
                    f'No tienes permisos para acceder a esta sección. '
                    f'Tu rol actual es: {request.user.get_rol_display()}. '
                    f'Se requiere uno de estos roles: {", ".join(roles_permitidos)}'
                )
                return redirect('proveedor')  

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
