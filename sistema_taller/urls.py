from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nucleo.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('clientes/', include('clientes.urls')),
    path('ordenes/', include('ordenes.urls')),
    path('inventario/', include('inventario.urls')),
    path('facturacion/', include('facturacion.urls')),
]
