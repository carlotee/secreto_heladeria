from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import LoginForm
from django.db import connection
import traceback
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from .models import Usuario
from django.contrib import messages

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        
        if form.is_valid():
            try:
                nuevo_usuario = form.save()
                
                print(f"✅ Usuario creado: {nuevo_usuario.username}")
                print(f"✅ Rol asignado: {nuevo_usuario.rol}")
                print(f"✅ Grupos: {[g.name for g in nuevo_usuario.groups.all()]}")
                
                messages.success(request, f'Usuario {nuevo_usuario.username} registrado exitosamente como {nuevo_usuario.get_rol_display()}')
                return redirect('login')
                
            except Exception as e:
                print(f"❌ Error al crear usuario: {str(e)}")
                print(traceback.format_exc())
                messages.error(request, f'Error al registrar usuario: {str(e)}')
        else:
            print("Formulario no válido")
            print("Errores:", form.errors)
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = RegistroForm()
    
    return render(request, 'accounts/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['password']

            try:
                usuario_obj = Usuario.objects.filter(username=usuario).first() or \
                                    Usuario.objects.filter(email=usuario).first()
                
                if usuario_obj:
                    user = authenticate(username=usuario_obj.username, password=password)
                    
                    if user is not None:
                        auth_login(request, user)
                        messages.success(request, f'¡Bienvenido de vuelta, {user.username}!') 
                        return redirect('dashboard')
                    else:
                        # Usamos messages.error para que base.html lo capture
                        messages.error(request, "Usuario o contraseña incorrectos")
                else:
                    messages.error(request, "Usuario o contraseña incorrectos")
                    
            except Exception as e:
                messages.error(request, "Error inesperado al iniciar sesión")
    else:
        form = LoginForm()

    # 👇 ¡ESTA ES LA PARTE IMPORTANTE! 👇
    # Aquí le decimos a la plantilla que oculte la barra de navegación.
    contexto = {
        'form': form,
        'hide_navbar': True  # <-- ESTA LÍNEA OCULTA EL NAV
    }
    return render(request, 'accounts/login.html', contexto)


def logout_view(request):
    logout(request)
    return redirect('login')