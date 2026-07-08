import os

apps = ['nucleo', 'usuarios', 'clientes', 'ordenes', 'inventario', 'facturacion']

for app in apps:
    os.makedirs(app, exist_ok=True)
    open(os.path.join(app, '__init__.py'), 'w').close()
    
    with open(os.path.join(app, 'apps.py'), 'w') as f:
        f.write(f"from django.apps import AppConfig\n\nclass {app.capitalize()}Config(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = '{app}'\n")
        
    with open(os.path.join(app, 'models.py'), 'w') as f:
        f.write("from django.db import models\n\n# Create your models here.\n")
        
    with open(os.path.join(app, 'admin.py'), 'w') as f:
        f.write("from django.contrib import admin\n\n# Register your models here.\n")
        
    with open(os.path.join(app, 'views.py'), 'w') as f:
        f.write("from django.shortcuts import render\n\n# Create your views here.\n")
        
    with open(os.path.join(app, 'urls.py'), 'w') as f:
        f.write("from django.urls import path\nfrom . import views\n\nurlpatterns = [\n]\n")
