from django.urls import path
from . import views

urlpatterns = [
    path('', views.ordenes_lista, name='ordenes_lista'),
    path('bandeja/', views.ordenes_bandeja, name='ordenes_bandeja'),
    path('<int:orden_id>/detalle/', views.orden_detalle, name='orden_detalle'),
    path('<int:orden_id>/cambiar-estado/', views.orden_cambiar_estado, name='orden_cambiar_estado'),
    path('refaccion/<int:refaccion_id>/eliminar/', views.orden_eliminar_refaccion, name='orden_eliminar_refaccion'),
]
