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
        default=1  # 👈 Esto evita que Django intente guardar un 0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.tipo_costo}"


class Costo(models.Model):
    descripcion = models.TextField()
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Valor del costo"
    )
    tipo_costo = models.ForeignKey(TipoCosto, on_delete=models.CASCADE)
    centro_costo = models.ForeignKey(Centro_Costos, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descripcion} - ${self.valor}"
