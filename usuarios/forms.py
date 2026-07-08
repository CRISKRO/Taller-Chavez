from django import forms
from .models import UsuarioPersonalizado

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'telefono']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'rol': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
