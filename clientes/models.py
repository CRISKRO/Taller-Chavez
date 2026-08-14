from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    color = models.CharField(max_length=30, default='Sin especificar')
    placa = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=17, unique=True, null=True, blank=True)
    kilometraje = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.color}) - {self.placa}"
