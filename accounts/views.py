from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import LoginForm
from .models import Registro
from django.db import connection
import traceback
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

def registro(request):
    try:
        print("=== REGISTRO ===")
        if request.method == 'POST':
            print("Método POST detectado")
            print("Datos POST:", request.POST)
            
            form = RegistroForm(request.POST)
            print("Formulario creado")
            
            if form.is_valid():
                print("Formulario válido")
                print("Datos limpios:", form.cleaned_data)
                
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT 1")
                        print("Conexión a BD OK")
                except Exception as db_error:
                    print("Error de conexión a BD:", str(db_error))
                    return render(request, 'accounts/registro.html', {
                        'form': form,
                        'error': f'Error de base de datos: {str(db_error)}'
                    })
                
                try:
                    print("Intentando crear registro manualmente...")
                    nuevo_registro = Registro(
                        usuario=form.cleaned_data['usuario'],
                        correo=form.cleaned_data['correo'],
                        contraseña=form.cleaned_data['contraseña'],
                        telefono=form.cleaned_data['telefono']
                    )
                    print("Objeto creado:", nuevo_registro)
                    
                    nuevo_registro.save()
                    print("¡Guardado exitosamente!")
                    
                    # ✅ CORREGIDO: pasa proveedor_id=1
                    return redirect('proveedor_dashboard', proveedor_id=1)
                    
                except Exception as save_error:
                    print("Error al guardar:", str(save_error))
                    print("Traceback del error:", traceback.format_exc())
                    
                    try:
                        print("Intentando con form.save()...")
                        registro = form.save()
                        print("Form.save() exitoso:", registro)
                        # ✅ CORREGIDO: pasa proveedor_id=1
                        return redirect('proveedor_dashboard', proveedor_id=1)
                    except Exception as form_save_error:
                        print("Error con form.save():", str(form_save_error))
                        return render(request, 'accounts/registro.html', {
                            'form': form,
                            'error': f'Error al guardar: {str(form_save_error)}'
                        })
            else:
                print("Formulario no válido")
                print("Errores del formulario:", form.errors)
                
        else:
            print("Método GET - mostrando formulario vacío")
            form = RegistroForm()
            
        return render(request, 'accounts/registro.html', {'form': form})
    
    except Exception as e:
        print("ERROR GENERAL en registro:", str(e))
        print("Traceback completo:", traceback.format_exc())
        return render(request, 'accounts/registro.html', {
            'form': RegistroForm(),
            'error': f'Error interno: {str(e)}'
        })


def login_view(request):
    User = get_user_model()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['password']

            usuario_obj = (Registro.objects.filter(usuario=usuario).first() or
                           Registro.objects.filter(correo=usuario).first())

            if usuario_obj and usuario_obj.contraseña == password:
                django_user, created = User.objects.get_or_create(username=usuario_obj.usuario)

                if created:
                    django_user.set_password(password)
                    django_user.email = usuario_obj.correo
                    django_user.save()

                user = authenticate(username=django_user.username, password=password)
                if user is not None:
                    auth_login(request, user)
                    print("✅ Login correcto, redirigiendo al dashboard...")
                    # ✅ CORREGIDO: pasa proveedor_id=1
                    return redirect('proveedor_dashboard', proveedor_id=1)
                else:
                    print("⚠️ Error al autenticar con Django")
                    form.add_error(None, "Error al autenticar el usuario")
            else:
                print("⚠️ Usuario o contraseña incorrectos")
                form.add_error(None, "Usuario o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
