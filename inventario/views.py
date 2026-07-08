from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ArticuloInventario
from .forms import ArticuloInventarioForm, CategoriaForm

@login_required
def inventario_lista(request):
    if request.method == 'POST':
        form = ArticuloInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo registrado exitosamente.')
            return redirect('inventario_lista')
    else:
        form = ArticuloInventarioForm()

    categoria_form = CategoriaForm()
    articulos = ArticuloInventario.objects.all().select_related('categoria')
    return render(request, 'inventario/lista.html', {'articulos': articulos, 'form': form, 'categoria_form': categoria_form})

@login_required
def categoria_crear(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
        else:
            messages.error(request, 'Error al crear categoría.')
    return redirect('inventario_lista')
