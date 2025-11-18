from django.db import models

# Create your models here.
class Periodo(models.Model):
    año = models.CharField(max_length=4)
    mes = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.mes} {self.año}"

    
class TipoCosto(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre

class Centro_Costos(models.Model):
    nombre = models.CharField(max_length=120, null=True, blank=True)
    tipo_costo = models.ForeignKey(
        'TipoCosto',
        on_delete=models.PROTECT,
        default=1 
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.tipo_costo}"


class Costo(models.Model):
    descripcion = models.CharField(max_length=255)
    tipo_costo = models.ForeignKey(TipoCosto, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['descripcion', 'tipo_costo'],
                name='unique_costo'
            )
        ]

    def __str__(self):
        return self.descripcion
