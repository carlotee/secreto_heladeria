from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class Factura(models.Model):
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return self.descripcion

