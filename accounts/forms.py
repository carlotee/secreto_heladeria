from django import forms
from .models import Registro

class LoginForm(forms.Form):
    usuario = forms.CharField(
        label="Usuario o Correo Electrónico",
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu usuario o correo'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'})
    )


from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    ROLES = [
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
        ('admin', 'Administrador'),
    ]

    rol = forms.ChoiceField(choices=ROLES, label="Rol")

    class Meta:
        model = Registro
        fields = ['usuario', 'correo', 'contraseña', 'telefono', 'rol']
        widgets = {
            'contraseña': forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'}),
            'usuario': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: +56912345678'}),
        }
        labels = {
            'usuario': 'Usuario',
            'correo': 'Correo electrónico',
            'contraseña': 'Contraseña',
            'telefono': 'Teléfono',
            'rol': 'Rol',
        }
