from django import forms
from .models import Cliente, Vehiculo

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'anio', 'color', 'placa', 'vin', 'kilometraje']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Ej. Toyota'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Ej. Corolla'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Ej. 2020'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Ej. Rojo Metálico'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Ej. ABC-1234'}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '17 caracteres (opcional/obligatorio según registro)'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Ej. 45000'}),
        }
