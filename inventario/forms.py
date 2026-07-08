from django import forms
from .models import ArticuloInventario, Categoria

class ArticuloInventarioForm(forms.ModelForm):
    class Meta:
        model = ArticuloInventario
        fields = ['codigo', 'nombre', 'descripcion', 'categoria', 'stock_actual', 'stock_minimo', 'precio_unitario', 'ubicacion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'})
        }
