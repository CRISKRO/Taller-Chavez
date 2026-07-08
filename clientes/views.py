from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm, VehiculoForm

@login_required
def clientes_lista(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado exitosamente.')
            return redirect('clientes_lista')
    else:
        form = ClienteForm()
        
    clientes = Cliente.objects.prefetch_related('vehiculos').all()
    # Pasa un formulario de vehículo vacío para el modal
    vehiculo_form = VehiculoForm()
    return render(request, 'clientes/lista.html', {'clientes': clientes, 'form': form, 'vehiculo_form': vehiculo_form})

@login_required
def vehiculo_crear(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.cliente = cliente
            vehiculo.save()
            messages.success(request, 'Vehículo registrado exitosamente.')
        else:
            messages.error(request, 'Error al registrar el vehículo. Revisa los datos.')
    return redirect('clientes_lista')
    