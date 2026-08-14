from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Factura
from .forms import FacturaForm, RegistrarPagoForm
from ordenes.models import OrdenServicio
from usuarios.decorators import role_required

@role_required(['ADMIN', 'RECEPCIONISTA'])
def facturacion_lista(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.calcular_totales()
            if factura.estado == 'PAGADO' and not factura.fecha_pago:
                factura.fecha_pago = timezone.now()
            factura.save()
            messages.success(request, f'Factura #{factura.id} generada exitosamente con cálculo automático de Mano de Obra y Refacciones.')
            return redirect('facturacion_lista')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = FacturaForm()

    facturas = Factura.objects.all().select_related('orden__cliente', 'orden__vehiculo').order_by('-fecha_emision')
    pago_form = RegistrarPagoForm()
    return render(request, 'facturacion/lista.html', {'facturas': facturas, 'form': form, 'pago_form': pago_form})

@role_required(['ADMIN', 'RECEPCIONISTA'])
def factura_registrar_pago(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        form = RegistrarPagoForm(request.POST, instance=factura)
        if form.is_valid():
            fact = form.save(commit=False)
            fact.estado = 'PAGADO'
            fact.fecha_pago = timezone.now()
            fact.save()
            messages.success(request, f'Pago registrado exitosamente para la Factura #{factura.id}. Comprobante PDF liberado.')
        else:
            messages.error(request, 'Error al registrar el pago.')
    return redirect('facturacion_lista')

@role_required(['ADMIN', 'RECEPCIONISTA'])
def generar_pdf_factura(request, factura_id):
    factura = get_object_or_404(Factura.objects.select_related('orden__cliente', 'orden__vehiculo').prefetch_related('orden__refacciones__articulo'), id=factura_id)
    
    # Quality Gate (TC-FAC-01): Bloqueo de PDF si la factura no está liquidada/pagada
    if factura.estado != 'PAGADO':
        messages.error(request, 'Quality Gate Financiero: El sistema bloquea la generación del comprobante PDF final hasta que la factura haya sido liquidada y pagada en su totalidad.')
        return redirect('facturacion_lista')

    template = get_template('facturacion/factura_pdf.html')
    context = {'factura': factura}
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.id}_OT_{factura.orden.numero}.pdf"'
    
    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        messages.error(request, 'Hubo un error al generar el PDF de la factura.')
        return redirect('facturacion_lista')
        
    return response
