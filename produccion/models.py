from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    

class OrdenCompra(models.Model):
    valor_total = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.valor_total
    

class DetalleCompra(models.Model):
    valor_unitario = models.CharField(max_length=100)
    cantidad_total = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.valor_unitario
