from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import LoginForm
from .models import Registro

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['password']
            try:
                usuario_obj = Registro.objects.get(usuario=usuario)
            except Registro.DoesNotExist:
                try:
                    usuario_obj = Registro.objects.get(correo=usuario)
                except Registro.DoesNotExist:
                    usuario_obj = None

            if usuario_obj and usuario_obj.contraseña == password:
                # Guardar sesión manualmente
                request.session['usuario_id'] = usuario_obj.id
                request.session['usuario_nombre'] = usuario_obj.usuario
                return redirect('dashboard')
            else:
                form.add_error(None, "Usuario o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            print("Datos limpios:", form.cleaned_data)
            registro = form.save()
            print("Guardado:", registro)
            return redirect('dashboard')
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})