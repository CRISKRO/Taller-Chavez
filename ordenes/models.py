from django.db import models
from clientes.models import Cliente, Vehiculo
from usuarios.models import UsuarioPersonalizado

class OrdenServicio(models.Model):
    ESTADOS = (
        ('RECIBIDO', 'Recibido'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
    )
    PRIORIDADES = (
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    )
    
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(UsuarioPersonalizado, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_asignadas')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='RECIBIDO')
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='MEDIA')
    descripcion = models.TextField()
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tiempo_estimado = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OT-{self.numero} - {self.vehiculo.placa}"
