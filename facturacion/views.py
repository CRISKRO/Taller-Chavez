from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Factura
from .forms import FacturaForm

@login_required
def facturacion_lista(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Factura creada exitosamente.')
            return redirect('facturacion_lista')
    else:
        form = FacturaForm()

    facturas = Factura.objects.all().select_related('orden__cliente')
    return render(request, 'facturacion/lista.html', {'facturas': facturas, 'form': form})

@login_required
def generar_pdf_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    template = get_template('facturacion/factura_pdf.html')
    context = {'factura': factura}
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.id}.pdf"'
    
    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        messages.error(request, 'Hubo un error al generar el PDF de la factura.')
        return redirect('facturacion_lista')
        
    return response
