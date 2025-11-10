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
    User = get_user_model()

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
                        print(f"✅ Login correcto para {user.username} (Rol: {user.rol})")
                        print(f"✅ Grupos: {[g.name for g in user.groups.all()]}")
                        return redirect('dashboard')
                    else:
                        print("⚠️ Contraseña incorrecta")
                        form.add_error(None, "Usuario o contraseña incorrectos")
                else:
                    print("⚠️ Usuario no encontrado")
                    form.add_error(None, "Usuario o contraseña incorrectos")
                    
            except Exception as e:
                print(f"❌ Error en login: {str(e)}")
                form.add_error(None, "Error al iniciar sesión")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')