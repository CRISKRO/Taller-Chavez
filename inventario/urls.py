from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.inventario_lista, name='inventario_lista'),
    path('categoria/nueva/', views.categoria_crear, name='categoria_crear'),
]
