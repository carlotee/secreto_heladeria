# proveedores/forms.py
from django import forms
from .models import Proveedor, Producto


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'rut', 'telefono', 'correo', 'direccion', 'ciudad']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569XXXXXXXX'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.cl'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
        }

        labels = {
            'nombre': 'Nombre',
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'correo': 'Correo electrónico',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio', 'min': 0}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock disponible', 'min': 0}),
        }

        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'stock': 'Stock disponible',
        }
