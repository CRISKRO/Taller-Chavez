from django import forms
from .models import OrdenServicio

class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = ['numero', 'cliente', 'vehiculo', 'mecanico', 'estado', 'prioridad', 'descripcion', 'costo_estimado', 'tiempo_estimado']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Ej. 005'}),
            'cliente': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'mecanico': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'prioridad': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'costo_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tiempo_estimado': forms.TextInput(attrs={'class': 'form-control'}),
        }
