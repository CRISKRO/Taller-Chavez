from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from .models import ArticuloInventario
from .forms import ArticuloInventarioForm, CategoriaForm
from usuarios.decorators import recepcionista_required

@recepcionista_required
def inventario_lista(request):
    if request.method == 'POST':
        form = ArticuloInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo registrado exitosamente.')
            return redirect('inventario_lista')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = ArticuloInventarioForm()

    categoria_form = CategoriaForm()
    articulos = ArticuloInventario.objects.all().select_related('categoria')
    
    # Métricas dinámicas de inventario
    total_items = articulos.count()
    bajo_stock_count = sum(1 for a in articulos if a.stock_actual <= a.stock_minimo)
    en_stock_count = total_items - bajo_stock_count
    
    valor_inventario = sum(a.stock_actual * a.precio_unitario for a in articulos)

    return render(request, 'inventario/lista.html', {
        'articulos': articulos,
        'form': form,
        'categoria_form': categoria_form,
        'total_items': total_items,
        'bajo_stock_count': bajo_stock_count,
        'en_stock_count': en_stock_count,
        'valor_inventario': valor_inventario,
    })

@recepcionista_required
def categoria_crear(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
        else:
            messages.error(request, 'Error al crear categoría.')
    return redirect('inventario_lista')
