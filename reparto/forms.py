from django import forms
from .models import Reparto

class RepartoForm(forms.ModelForm):
    class Meta:
        model = Reparto
        fields = ['valor','fecha_reparto','fecha_ingreso','usuario']
        widgets = {
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_reparto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
        }