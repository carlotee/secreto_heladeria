from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return f"{self.username} ({self.email})"
    
class Registro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="registros")
    accion = models.CharField(max_length=255) 
    fecha = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.usuario.username} - {self.accion} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
