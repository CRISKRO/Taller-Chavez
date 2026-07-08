from django.shortcuts import render, redirect
from .models import OrdenServicio
from .forms import OrdenServicioForm

def ordenes_lista(request):
    if request.method == 'POST':
        form = OrdenServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ordenes_lista')
    else:
        form = OrdenServicioForm()

    ordenes = OrdenServicio.objects.all().select_related('cliente', 'vehiculo', 'mecanico')
    return render(request, 'ordenes/lista.html', {'ordenes': ordenes, 'form': form})
