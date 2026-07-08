from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioPersonalizado(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('MECANICO', 'Mecánico'),
        ('RECEPCIONISTA', 'Recepcionista'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='RECEPCIONISTA')
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_rol_display()})"
