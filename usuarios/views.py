from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import UsuarioPersonalizado
from .forms import UsuarioForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def usuarios_lista(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Creamos el usuario pero con una contraseña genérica (o podríamos añadir el campo password)
            usuario = form.save(commit=False)
            usuario.set_password('Taller123') # Contraseña por defecto
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios_lista')
    else:
        form = UsuarioForm()
        
    usuarios = UsuarioPersonalizado.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios, 'form': form})

def usuario_editar(request, pk):
    usuario = get_object_or_404(UsuarioPersonalizado, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios_lista')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'usuario': usuario, 'accion': 'Editar'})

def usuario_eliminar(request, pk):
    usuario = get_object_or_404(UsuarioPersonalizado, pk=pk)
    if request.method == 'POST':
        if usuario == request.user:
            messages.error(request, 'No puedes eliminar tu propio usuario.')
        else:
            usuario.delete()
            messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('usuarios_lista')
    return render(request, 'usuarios/usuario_confirm_delete.html', {'usuario': usuario})

