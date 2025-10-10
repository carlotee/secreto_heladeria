from django.db import models
from proveedores.models import Proveedor


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, null=True, blank=True, related_name="productos"
    )

    def __str__(self):
        return self.nombre

class Costo(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='costos')
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - ${self.valor}"