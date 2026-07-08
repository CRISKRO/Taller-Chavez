from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.usuarios_lista, name='usuarios_lista'),
    path('editar/<int:pk>/', views.usuario_editar, name='usuario_editar'),
    path('eliminar/<int:pk>/', views.usuario_eliminar, name='usuario_eliminar'),
]
