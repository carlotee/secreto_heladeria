import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Periodo, TipoCosto, Centro_Costos, Costo, TransaccionCompra
from .validators import validar_solo_letras

def validar_solo_letras(valor):
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]+$', valor):
        raise ValidationError('Este campo solo puede contener letras y espacios.')

class PeriodoForm(forms.ModelForm):
    """Formulario para crear o actualizar un periodo"""
    class Meta:
        model = Periodo
        fields = ['año', 'mes']
        widgets = {
            'año': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el año',
                'min': 2000
            }),
            'mes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el mes',
                'min': 1
            }),
        }

class TipoCostoForm(forms.ModelForm):
    """Formulario para crear o actualizar una categoría (TipoCosto)"""
    class Meta:
        model = TipoCosto
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la categoría'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría',
                'maxlength': 30, 
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        
        if nombre:
            if len(nombre) < 5:
                raise ValidationError("El nombre de la categoría debe tener un mínimo de 5 caracteres.")
            
            if len(nombre) > 30:
                raise ValidationError("El nombre de la categoría no puede exceder los 30 caracteres.")

            validar_solo_letras(nombre)
            
            qs = TipoCosto.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Ya existe una categoría con ese nombre.")
                
        return nombre

class CentroCostosForm(forms.ModelForm):
    """Formulario para crear o actualizar un centro de costos"""
    class Meta:
        model = Centro_Costos
        fields = ['nombre', 'tipo_costo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del centro de costos'
            }),
            'tipo_costo': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class CostoForm(forms.ModelForm):
    """Formulario para crear o actualizar un Item Costo"""
    class Meta:
        model = Costo
        fields = ['descripcion', 'tipo_costo']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'maxlength': 35, 
            }),
            'tipo_costo': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        
        if descripcion:
            if len(descripcion) < 5:
                raise forms.ValidationError("La descripción debe tener un mínimo de 5 caracteres.")
            
            if len(descripcion) > 35:
                raise forms.ValidationError("La descripción no puede exceder los 35 caracteres.")
            
            validar_solo_letras(descripcion) 
            
        return descripcion
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')
        tipo_costo = cleaned_data.get('tipo_costo')

        if descripcion and tipo_costo:
            qs = Costo.objects.filter(descripcion=descripcion, tipo_costo=tipo_costo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Item Costo con esta Descripción y Categoría ya existe.")
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')
        tipo_costo = cleaned_data.get('tipo_costo')

        if descripcion and tipo_costo:
            qs = Costo.objects.filter(descripcion=descripcion, tipo_costo=tipo_costo)
            
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
                
            if qs.exists():
                raise forms.ValidationError("Item Costo con esta Descripción y Categoría ya existe.")
                
        return cleaned_data

class ConfirmarEliminarCostoForm(forms.Form):
    """Formulario simple para confirmar la eliminación de un Item Costo"""
    confirmar = forms.BooleanField(
        required=True,
        label="Confirmo la eliminación de este Item Costo",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
class TransaccionCompraForm(forms.ModelForm):
    """Formulario para crear o actualizar una transacción"""
    class Meta:
        model = TransaccionCompra
        fields = ['nombre', 'costo', 'proveedor', 'costo_total'] 
        
        labels = {
            'costo': 'Item Costo',
            'proveedor': 'Proveedor', 
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 40,
            }),
            'costo': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'costo_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        
        if nombre:
            if len(nombre) < 5:
                raise ValidationError("El nombre de la transacción debe tener un mínimo de 5 caracteres.")
            
            if len(nombre) > 40:
                raise ValidationError("El nombre de la transacción no puede exceder los 40 caracteres.")
            
            validar_solo_letras(nombre)
            
        return nombre

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        costo = cleaned_data.get('costo')

        if nombre and costo:
            qs = TransaccionCompra.objects.filter(nombre=nombre, costo=costo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Ya existe una transacción con este Nombre y Item Costo.")
        return cleaned_data

    def clean_costo_total(self):
        costo_total = self.cleaned_data.get('costo_total')

        if costo_total is not None:
            if costo_total <= 0:
                raise ValidationError("El costo total debe ser mayor a 0")

            str_costo = f"{costo_total:.2f}" 
            if '.' in str_costo:
                entero = str_costo.split('.')[0] 
            else:
                entero = str_costo
                
            if len(entero) > 10:
                raise ValidationError("El costo total no puede tener más de 10 dígitos antes del punto decimal")

        return costo_total