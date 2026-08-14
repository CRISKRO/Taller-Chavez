from django import forms
from .models import OrdenServicio, RefaccionOrden
from usuarios.models import UsuarioPersonalizado

class OrdenServicioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo mecánicos para la asignación
        self.fields['mecanico'].queryset = UsuarioPersonalizado.objects.filter(rol='MECANICO', is_active=True)

    class Meta:
        model = OrdenServicio
        fields = ['numero', 'cliente', 'vehiculo', 'mecanico', 'prioridad', 'descripcion', 'costo_estimado', 'tiempo_estimado', 'anticipo', 'foto_inicial']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Ej. 005'}),
            'cliente': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'mecanico': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required', 'placeholder': 'Descripción de falla o servicio solicitado...'}),
            'costo_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tiempo_estimado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 2 horas / 1 día'}),
            'anticipo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'foto_inicial': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class DiagnosticoMecanicoForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = ['diagnostico', 'observaciones', 'mano_de_obra', 'foto_final', 'estado']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Diagnóstico técnico del problema detectado...'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observaciones técnicas adicionales...'}),
            'mano_de_obra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'foto_final': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class RefaccionOrdenForm(forms.ModelForm):
    class Meta:
        model = RefaccionOrden
        fields = ['articulo', 'cantidad', 'precio_unitario']
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Precio unitario'}),
        }
