from django.db import models
from decimal import Decimal
from clientes.models import Cliente, Vehiculo
from usuarios.models import UsuarioPersonalizado
from inventario.models import ArticuloInventario

class OrdenServicio(models.Model):
    ESTADOS = (
        ('RECIBIDO', 'Recibido'),
        ('EN_PROCESO', 'En Proceso'),
        ('CONCLUIDO', 'Concluido'),
        ('COMPLETADO', 'Concluido'), # Compatibilidad
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
    descripcion = models.TextField(help_text="Motivo de ingreso o falla reportada por el cliente.")
    diagnostico = models.TextField(blank=True, null=True, help_text="Diagnóstico técnico registrado por el mecánico.")
    observaciones = models.TextField(blank=True, null=True, help_text="Observaciones adicionales de reparación.")
    
    # Evidencia fotográfica
    foto_inicial = models.ImageField(upload_to='evidencias/inicial/', blank=True, null=True)
    foto_final = models.ImageField(upload_to='evidencias/final/', blank=True, null=True)
    
    # Costos
    mano_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tiempo_estimado = models.CharField(max_length=50, blank=True, null=True)
    
    # Control transaccional
    inventario_descontado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    @property
    def total_refacciones(self):
        return sum(item.subtotal for item in self.refacciones.all())

    @property
    def total_calculado(self):
        return self.mano_de_obra + self.total_refacciones

    @property
    def saldo_pendiente(self):
        saldo = self.total_calculado - self.anticipo
        return max(saldo, Decimal('0.00'))

    def __str__(self):
        return f"OT-{self.numero} - {self.vehiculo.placa} ({self.get_estado_display()})"


class RefaccionOrden(models.Model):
    orden = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, related_name='refacciones')
    articulo = models.ForeignKey(ArticuloInventario, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return Decimal(self.cantidad) * self.precio_unitario

    def save(self, *args, **kwargs):
        if not self.precio_unitario and self.articulo:
            self.precio_unitario = self.articulo.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad}x {self.articulo.nombre} (OT-{self.orden.numero})"
