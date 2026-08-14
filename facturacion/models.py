from django.db import models
from decimal import Decimal
from ordenes.models import OrdenServicio

class Factura(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente de Pago'),
        ('PAGADO', 'Liquidado / Pagado'),
    )
    METODOS_PAGO = (
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA_CREDITO', 'Tarjeta de Crédito'),
        ('TARJETA_DEBITO', 'Tarjeta de Débito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('OTRO', 'Otro'),
    )

    orden = models.OneToOneField(OrdenServicio, on_delete=models.CASCADE, related_name='factura')
    mano_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    costo_refacciones = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    anticipo_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, blank=True, null=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    def calcular_totales(self):
        if self.orden:
            self.mano_de_obra = self.orden.mano_de_obra
            self.costo_refacciones = self.orden.total_refacciones
            self.subtotal = self.mano_de_obra + self.costo_refacciones
            self.iva = round(self.subtotal * Decimal('0.16'), 2)
            self.total = self.subtotal + self.iva
            self.anticipo_aplicado = self.orden.anticipo
            self.saldo_pendiente = max(self.total - self.anticipo_aplicado, Decimal('0.00'))

    def save(self, *args, **kwargs):
        if not self.total or self.total == Decimal('0.00'):
            self.calcular_totales()
        else:
            if not self.subtotal:
                self.subtotal = round(self.total / Decimal('1.16'), 2)
                self.iva = self.total - self.subtotal
            if not self.saldo_pendiente and self.orden:
                self.anticipo_aplicado = self.orden.anticipo
                self.saldo_pendiente = max(self.total - self.anticipo_aplicado, Decimal('0.00'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura #{self.id} - OT-{self.orden.numero} ({self.get_estado_display()})"
