from django.db import models

# Create your models here.
class Periodo(models.Model):
    año = models.CharField(max_length=4)
    mes = models.CharField(max_length=10)

    
class TipoCosto(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre

class Centro_Costos(models.Model):
    TIPO_COSTO_CHOICES = [
        ("Fijo", "Fijo")
        ("Variable","Variable"),
    ]
    nombre = models.CharField(max_length=120)
    tipo_costo = models.CharField(max_length=10, choices=TIPO_COSTO_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.tipo_costo}"


class Costo(models.Model):
    descripcion = models.CharField(max_length=120)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    tipo_costo = models.ForeignKey(TipoCosto, on_delete=models.PROTECT)
    centro_costo = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, null=True, blank=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.descripcion} - {self.valor} - {self.tipo_costo.nombre}"
