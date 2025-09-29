from django import forms
from .models import GastosComunes

class GastosComunesForm(forms.ModelForm):
    class Meta:
        model = GastosComunes
        fields = ['nombre']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }