from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import OrdenServicio, RefaccionOrden
from .forms import OrdenServicioForm, DiagnosticoMecanicoForm, RefaccionOrdenForm
from usuarios.decorators import role_required, mecanico_required

@login_required
def ordenes_lista(request):
    if request.user.rol == 'MECANICO':
        # Si un mecánico entra a la lista general, se le redirige a su bandeja técnica
        return redirect('ordenes_bandeja')

    if request.method == 'POST':
        form = OrdenServicioForm(request.POST, request.FILES)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.estado = 'RECIBIDO' # Siempre inicia en Recibido
            orden.save()
            messages.success(request, f'Orden de Servicio OT-{orden.numero} creada exitosamente.')
            return redirect('orden_detalle', orden_id=orden.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = OrdenServicioForm()

    ordenes = OrdenServicio.objects.all().select_related('cliente', 'vehiculo', 'mecanico').order_by('-fecha_creacion')
    return render(request, 'ordenes/lista.html', {'ordenes': ordenes, 'form': form})

@mecanico_required
def ordenes_bandeja(request):
    """
    Bandeja técnica exclusiva del mecánico logueado (TC-ORD-01).
    """
    if request.user.rol == 'ADMIN':
        ordenes = OrdenServicio.objects.all().select_related('cliente', 'vehiculo', 'mecanico').order_by('-fecha_creacion')
    else:
        ordenes = OrdenServicio.objects.filter(mecanico=request.user).select_related('cliente', 'vehiculo').order_by('-fecha_creacion')

    total_asignadas = ordenes.count()
    en_proceso_count = sum(1 for o in ordenes if o.estado == 'EN_PROCESO')

    return render(request, 'ordenes/bandeja_mecanico.html', {
        'ordenes': ordenes,
        'total_asignadas': total_asignadas,
        'en_proceso_count': en_proceso_count,
    })

@login_required
def orden_detalle(request, orden_id):
    orden = get_object_or_404(OrdenServicio.objects.select_related('cliente', 'vehiculo', 'mecanico').prefetch_related('refacciones__articulo'), id=orden_id)
    
    # Validar que si es mecánico solo pueda ver sus órdenes asignadas
    if request.user.rol == 'MECANICO' and orden.mecanico != request.user:
        messages.error(request, 'No tienes asignada esta orden de trabajo.')
        return redirect('ordenes_bandeja')

    diagnostico_form = DiagnosticoMecanicoForm(instance=orden)
    refaccion_form = RefaccionOrdenForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'guardar_diagnostico':
            form = DiagnosticoMecanicoForm(request.POST, request.FILES, instance=orden)
            if form.is_valid():
                form.save()
                messages.success(request, 'Diagnóstico y detalles técnicos guardados correctamente.')
                return redirect('orden_detalle', orden_id=orden.id)
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
                        
        elif action == 'agregar_refaccion':
            r_form = RefaccionOrdenForm(request.POST)
            if r_form.is_valid():
                refaccion = r_form.save(commit=False)
                refaccion.orden = orden
                if not refaccion.precio_unitario:
                    refaccion.precio_unitario = refaccion.articulo.precio_unitario
                refaccion.save()
                messages.success(request, f'Refacción {refaccion.articulo.nombre} agregada a la orden.')
                return redirect('orden_detalle', orden_id=orden.id)

    return render(request, 'ordenes/orden_detalle.html', {
        'orden': orden,
        'diagnostico_form': diagnostico_form,
        'refaccion_form': refaccion_form,
    })

@login_required
def orden_cambiar_estado(request, orden_id):
    """
    Quality Gate de Transición de Estados (TC-ORD-02) y Descuento Atómico de Inventario (TC-INV-01).
    """
    orden = get_object_or_404(OrdenServicio, id=orden_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        
        # Validar saltos inválidos (TC-ORD-02)
        if orden.estado == 'RECIBIDO' and nuevo_estado in ['CONCLUIDO', 'COMPLETADO']:
            messages.error(request, 'Violación de Quality Gate (TC-ORD-02): No se puede pasar de "Recibido" directamente a "Concluido". Debe pasar primero a "En Proceso" y contar con un diagnóstico.')
            return redirect('orden_detalle', orden_id=orden.id)
        
        if nuevo_estado in ['CONCLUIDO', 'COMPLETADO']:
            if not orden.diagnostico or len(orden.diagnostico.strip()) == 0:
                messages.error(request, 'No es posible concluir la orden sin haber registrado previamente el Diagnóstico Técnico.')
                return redirect('orden_detalle', orden_id=orden.id)
            
            # Lógica Transaccional Atómica de Descuento de Inventario (TC-INV-01)
            try:
                with transaction.atomic():
                    if not orden.inventario_descontado:
                        for ref in orden.refacciones.select_related('articulo').all():
                            articulo = ref.articulo
                            if articulo.stock_actual < ref.cantidad:
                                raise ValueError(f"Stock insuficiente para {articulo.nombre}. Disponible: {articulo.stock_actual}, Requerido: {ref.cantidad}")
                            articulo.stock_actual -= ref.cantidad
                            articulo.save()
                        orden.inventario_descontado = True
                    
                    orden.estado = 'CONCLUIDO'
                    orden.save()
                    messages.success(request, f'Orden OT-{orden.numero} CONCLUIDA exitosamente. El inventario ha sido actualizado de forma atómica.')
            except ValueError as e:
                messages.error(request, f"Error de inventario: {str(e)}")
            except Exception as e:
                messages.error(request, f"Error al procesar el cierre de la orden: {str(e)}")
                
        elif nuevo_estado == 'EN_PROCESO':
            orden.estado = 'EN_PROCESO'
            orden.save()
            messages.success(request, f'Orden OT-{orden.numero} iniciada. Estado actual: En Proceso.')
            
        elif nuevo_estado == 'RECIBIDO':
            orden.estado = 'RECIBIDO'
            orden.save()
            messages.info(request, f'Orden OT-{orden.numero} marcada como Recibida.')
            
    return redirect('orden_detalle', orden_id=orden.id)

@login_required
def orden_eliminar_refaccion(request, refaccion_id):
    refaccion = get_object_or_404(RefaccionOrden, id=refaccion_id)
    orden_id = refaccion.orden.id
    
    if refaccion.orden.estado in ['CONCLUIDO', 'COMPLETADO']:
        messages.error(request, 'No se pueden modificar refacciones en una orden ya concluida.')
    else:
        refaccion.delete()
        messages.success(request, 'Refacción eliminada de la orden.')
        
    return redirect('orden_detalle', orden_id=orden_id)
