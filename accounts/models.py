from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    email = models.EmailField(unique=True)
    numero = models.CharField(max_length=15, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return f"{self.username} ({self.email})"
    
class Registro(models.Model):
    usuario = models.CharField(max_length=50)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=128)
    numero = models.CharField(max_length=15)
    fecha = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.usuario} - {self.correo} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"