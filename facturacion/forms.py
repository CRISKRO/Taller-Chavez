from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'total', 'metodo_pago', 'estado', 'notas']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'estado': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
