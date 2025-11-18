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
                'placeholder': 'Nombre de la categoría'
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
    class Meta:
        model = Costo
        fields = ['descripcion', 'tipo_costo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_costo': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')
        tipo_costo = cleaned_data.get('tipo_costo')

        if descripcion and tipo_costo:
            qs = Costo.objects.filter(descripcion=descripcion, tipo_costo=tipo_costo)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    "Item Costo con esta Descripción y Categoría ya existe."
                )

        return cleaned_data





class ConfirmarEliminarCostoForm(forms.Form):
    """Formulario simple para confirmar la eliminación de un costo"""
    confirmar = forms.BooleanField(
        required=True,
        label="Confirmo la eliminación de este costo",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
