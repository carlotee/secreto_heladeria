from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import LoginForm
from .models import Registro
from django.db import connection
import traceback

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

            if usuario_obj and usuario_obj.verificar_contraseña(password):
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
    try:
        print("=== INICIO REGISTRO ===")
        if request.method == 'POST':
            print("Método POST detectado")
            print("Datos POST:", request.POST)
            
            form = RegistroForm(request.POST)
            print("Formulario creado")
            
            if form.is_valid():
                print("Formulario válido")
                print("Datos limpios:", form.cleaned_data)
                
                # Verificar conexión a BD
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
                
                # Intentar guardar manualmente
                try:
                    print("Intentando crear registro manualmente...")
                    nuevo_registro = Registro(
                        usuario=form.cleaned_data['usuario'],
                        correo=form.cleaned_data['correo'],
                        contraseña=form.cleaned_data['contraseña'],
                        telefono=form.cleaned_data['telefono']
                    )
                    print("Objeto creado:", nuevo_registro)
                    
                    # Guardar
                    nuevo_registro.save()
                    print("¡Guardado exitosamente!")
                    
                    return redirect('dashboard')
                    
                except Exception as save_error:
                    print("Error al guardar:", str(save_error))
                    print("Traceback del error:", traceback.format_exc())
                    
                    # Intentar con form.save()
                    try:
                        print("Intentando con form.save()...")
                        registro = form.save()
                        print("Form.save() exitoso:", registro)
                        return redirect('dashboard')
                    except Exception as form_save_error:
                        print("Error con form.save():", str(form_save_error))
                        return render(request, 'accounts/registro.html', {
                            'form': form,
                            'error': f'Error al guardar: {str(form_save_error)}'
                        })
            else:
                print("Formulario NO válido")
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