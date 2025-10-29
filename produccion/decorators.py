from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def rol_requerido(*roles_permitidos):
    """
    Decorador que verifica si el usuario tiene uno de los roles permitidos.
    Verifica tanto el campo 'rol' como los grupos de Django.
    
    Uso: @rol_requerido('Proveedor', 'Administrador')
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
                    f'No tienes permisos para realizar esta acción. Tu rol actual es: {request.user.get_rol_display()}. '
                    f'Se requiere uno de estos roles: {", ".join(roles_permitidos)}'
                )
                return redirect('producto')  
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator