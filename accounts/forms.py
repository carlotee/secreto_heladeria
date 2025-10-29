from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario

class LoginForm(forms.Form):
    usuario = forms.CharField(
        label="Usuario o Correo Electrónico",
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu usuario o correo'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'})
    )


class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'})
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'numero', 'rol', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Ej: +56912345678'}),
        }
        labels = {
            'username': 'Usuario',
            'email': 'Correo electrónico',
            'numero': 'Teléfono',
            'rol': 'Rol',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password']) 
        
        if commit:
            user.save()
        
        return user