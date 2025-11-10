from django import forms
from .models import Producto
from proveedores.models import Proveedor
from .models import Costo

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'proveedor']

        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'stock': 'Stock disponible',
            'proveedor': 'Proveedor', 
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
            'proveedor': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class CostoForm(forms.ModelForm):
    class Meta:
        model = Costo
        fields = '__all__'

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor <= 0:
            raise forms.ValidationError("El valor del costo debe ser mayor que 0.")
        return valor
