from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=120)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, null=True)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Proveedor: {self.nombre}, RUT: {self.rut}"