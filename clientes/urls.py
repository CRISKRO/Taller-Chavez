from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes_lista, name='clientes_lista'),
    path('vehiculo/nuevo/<int:cliente_id>/', views.vehiculo_crear, name='vehiculo_crear'),
]
