from django.db import models
from ordenes.models import OrdenServicio

class Factura(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
    )
    orden = models.OneToOneField(OrdenServicio, on_delete=models.CASCADE, related_name='factura')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    METODOS_PAGO = (
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA_CREDITO', 'Tarjeta de Crédito'),
        ('TARJETA_DEBITO', 'Tarjeta de Débito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('OTRO', 'Otro'),
    )
    fecha_emision = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        from decimal import Decimal
        if self.total:
            # Calculamos subtotal e IVA (asumiendo 12% según el template)
            self.subtotal = round(self.total / Decimal('1.12'), 2)
            self.iva = self.total - self.subtotal
        else:
            self.subtotal = Decimal('0.00')
            self.iva = Decimal('0.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura #{self.id} - OT-{self.orden.numero}"
