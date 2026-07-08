from django.urls import path
from . import views

urlpatterns = [
    path('', views.ordenes_lista, name='ordenes_lista'),
]
