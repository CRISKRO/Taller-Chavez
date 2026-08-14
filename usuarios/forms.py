from django import forms
from django.core.exceptions import ValidationError
from .models import UsuarioPersonalizado

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'}),
        required=False,
        label='Contraseña',
        help_text='Mínimo 8 caracteres.'
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'telefono', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'rol': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.pk and not password:
            raise ValidationError("La contraseña es requerida para nuevos usuarios.")
        if password:
            if len(password) < 8:
                raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return password
