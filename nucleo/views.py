from django.shortcuts import render
# 1. Importa el decorador login_required
from django.contrib.auth.decorators import login_required

# 2. Añade @login_required justo encima de tu vista
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
