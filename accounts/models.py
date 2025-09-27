from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    username = models.CharField(max_length=191, unique=True)
    email = models.EmailField(unique=True, max_length=191)
    numero = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.username} ({self.email})"

class Registro(models.Model):
    usuario = models.CharField(max_length=50, db_column='usuario')
    correo = models.EmailField(max_length=191, db_column='correo')
    contraseña = models.CharField(max_length=128, db_column='contraseña')
    telefono = models.CharField(max_length=15, db_column='telefono')

    class Meta:
        db_table = 'login'

    def __str__(self):
        return f"{self.usuario} - {self.correo}"
