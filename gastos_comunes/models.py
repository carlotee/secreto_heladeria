from django.db import models

# Create your models here.
class GastosComunes(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class BoletaGC(models.Model):
    valor = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    gastosComunes = models.ForeignKey(GastosComunes, on_delete=models.CASCADE)

    def __str__(self):
        return self.valor
    