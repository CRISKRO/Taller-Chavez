from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ordenes.models import OrdenServicio
from clientes.models import Cliente
from inventario.models import ArticuloInventario
from facturacion.models import Factura

@login_required
def dashboard(request):
    # Métricas en tiempo real
    ordenes_activas = OrdenServicio.objects.filter(estado__in=['RECIBIDO', 'EN_PROCESO'])
    ordenes_activas_count = ordenes_activas.count()
    
    facturas_pendientes = Factura.objects.filter(estado='PENDIENTE')
    pendiente_cobro = sum(f.saldo_pendiente for f in facturas_pendientes)
    
    articulos = ArticuloInventario.objects.all()
    bajo_stock_count = sum(1 for a in articulos if a.stock_actual <= a.stock_minimo)
    
    clientes_count = Cliente.objects.count()
    
    ordenes_recientes = OrdenServicio.objects.all().select_related('cliente', 'vehiculo', 'mecanico').order_by('-fecha_creacion')[:8]

    return render(request, 'dashboard.html', {
        'ordenes_activas_count': ordenes_activas_count,
        'pendiente_cobro': pendiente_cobro,
        'bajo_stock_count': bajo_stock_count,
        'clientes_count': clientes_count,
        'ordenes_recientes': ordenes_recientes,
    })
