from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(blank=True)  # <- importante
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)  # <- importante
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre