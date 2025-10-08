from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Producto: {self.nombre}, Precio: {self.precio}"