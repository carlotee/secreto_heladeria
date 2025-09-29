from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Ventas(models.Model):
    valor_total = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return self.valor_total
    
class DetalleVenta(models.Model):
    valor_unitario = models.CharField(max_length=100)
    ventas = models.ForeignKey(Ventas, on_delete=models.CASCADE)

    def __str__(self):
        return self.valor_unitario
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Reparto(models.Model):
    valor = models.CharField(max_length=100)
    fecha_reparto = models.DateTimeField()
    fecha_ingreso = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.valor
