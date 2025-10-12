from django import forms
from .models import Producto
from proveedores.models import Proveedor  # 🔹 Import necesario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'proveedor']  # 🔹 Agregamos proveedor aquí

        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'stock': 'Stock disponible',
            'proveedor': 'Proveedor',  # 🔹 Nuevo label
        }

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del producto',
                'rows': 3,
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio',
                'min': 0,
                'step': 0.01,
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad disponible',
                'min': 0,
            }),
            # 🔹 Este widget crea un desplegable con todos los proveedores existentes
            'proveedor': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
