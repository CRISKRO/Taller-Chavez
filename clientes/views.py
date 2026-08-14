from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Vehiculo
from .forms import ClienteForm, VehiculoForm
from usuarios.decorators import recepcionista_required

@recepcionista_required
def clientes_lista(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado exitosamente.')
            return redirect('clientes_lista')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = ClienteForm()
        
    clientes = Cliente.objects.prefetch_related('vehiculos').all()
    vehiculo_form = VehiculoForm()
    return render(request, 'clientes/lista.html', {'clientes': clientes, 'form': form, 'vehiculo_form': vehiculo_form})

@recepcionista_required
def vehiculo_crear(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.cliente = cliente
            vehiculo.save()
            messages.success(request, f'Vehículo {vehiculo.marca} {vehiculo.modelo} registrado exitosamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    return redirect('clientes_lista')

@recepcionista_required
def vehiculo_historial(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo.objects.select_related('cliente'), id=vehiculo_id)
    ordenes = vehiculo.ordenservicio_set.all().select_related('mecanico').prefetch_related('refacciones__articulo').order_by('-fecha_creacion')
    return render(request, 'clientes/historia_clinica.html', {'vehiculo': vehiculo, 'ordenes': ordenes})
    