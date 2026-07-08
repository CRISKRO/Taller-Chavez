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
        fields = ['marca', 'modelo', 'anio', 'placa', 'kilometraje']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }
