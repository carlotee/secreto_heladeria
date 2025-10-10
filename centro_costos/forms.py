from django import forms
from .models import Periodo, TipoCosto, Centro_Costos, Costo


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
    """Formulario para crear o actualizar un tipo de costo"""
    class Meta:
        model = TipoCosto
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del tipo de costo'
            }),
        }


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
    """Formulario para crear o actualizar un costo"""
    class Meta:
        model = Costo
        fields = ['descripcion', 'valor', 'tipo_costo', 'centro_costo', 'periodo']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del costo'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Valor del costo',
                'min': 0
            }),
            'tipo_costo': forms.Select(attrs={'class': 'form-control'}),
            'centro_costo': forms.Select(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
        }



class ConfirmarEliminarCostoForm(forms.Form):
    """Formulario simple para confirmar la eliminación de un costo"""
    confirmar = forms.BooleanField(
        required=True,
        label="Confirmo la eliminación de este costo",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
