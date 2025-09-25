from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['password']

            user = authenticate(request, username=usuario, password=password)
            if user is None:
               
                from accounts.models import Usuario
                try:
                    usuario_obj = Usuario.objects.get(email=usuario)
                    user = authenticate(request, username=usuario_obj.username, password=password)
                except Usuario.DoesNotExist:
                    user = None

            if user is not None:
                auth_login(request, user)
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
            form.save()  
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})