from django.db import models
from proveedores.models import Proveedor
from django.utils import timezone


class Producto(models.Model):
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='productos',
        blank=True,
        null=True
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.proveedor:
            return f"{self.nombre} ({self.proveedor.nombre})"
        return self.nombre


class Costo(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='costos'
    )
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  

    def eliminar(self):
        """Borrado lógico del costo"""
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.descripcion} - ${self.valor}"
