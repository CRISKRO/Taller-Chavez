from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import UsuarioPersonalizado
from .forms import UsuarioForm
from .decorators import admin_required

def get_role_redirect_url(user):
    if user.rol == 'MECANICO':
        return 'ordenes_bandeja'
    return 'dashboard'

def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_role_redirect_url(request.user))
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect(get_role_redirect_url(user))
            else:
                messages.error(request, 'Credenciales inválidas.')
        else:
            messages.error(request, 'Credenciales inválidas.')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

@admin_required
def usuarios_lista(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                usuario.set_password(password)
            else:
                usuario.set_password('Taller123')
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios_lista')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UsuarioForm()
        
    usuarios = UsuarioPersonalizado.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios, 'form': form})

@admin_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(UsuarioPersonalizado, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user_obj = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user_obj.set_password(password)
            user_obj.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios_lista')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'usuario': usuario, 'accion': 'Editar'})

@admin_required
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

