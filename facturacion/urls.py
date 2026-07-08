from django.urls import path
from . import views

urlpatterns = [
    path('', views.facturacion_lista, name='facturacion_lista'),
    path('pdf/<int:factura_id>/', views.generar_pdf_factura, name='generar_pdf_factura'),
]
