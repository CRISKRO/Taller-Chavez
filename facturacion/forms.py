from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'metodo_pago', 'estado', 'notas']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas de facturación...'}),
        }


class RegistrarPagoForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['metodo_pago', 'notas']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Detalles de la transacción o referencia...'}),
        }
 



    