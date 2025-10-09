from django.db import models
from proveedores.models import Producto  # relación cruzada

class Costo(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='costos')
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - ${self.valor}"
