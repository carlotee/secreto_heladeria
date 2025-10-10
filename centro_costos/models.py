from django.db import models
from produccion.models import Costo

# Create your models here.
class Periodo(models.Model):
    año = models.CharField(max_length=4)
    mes = models.CharField(max_length=10)

    
class TipoCosto(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre

class Centro_Costos(models.Model):
    nombre = models.CharField(max_length=120,null=True, blank=True)
    tipo_costo = models.ForeignKey(TipoCosto, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.tipo_costo}"


class Costo(models.Model):
    descripcion = models.CharField(max_length=120)
    costo = models.ForeignKey(Costo, on_delete=models.CASCADE, related_name='costos')
    tipo_costo = models.ForeignKey(TipoCosto, on_delete=models.PROTECT)
    centro_costo = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, null=True, blank=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.descripcion} - {self.valor} - {self.tipo_costo.nombre}"
