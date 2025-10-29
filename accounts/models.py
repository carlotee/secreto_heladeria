from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('proveedor', 'Proveedor'),
        ('cliente', 'Cliente'),
    ]

    username = models.CharField(max_length=191, unique=True)
    email = models.EmailField(unique=True, max_length=191)
    numero = models.CharField(max_length=15, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sincronizar_grupo()
    
    def sincronizar_grupo(self):
        """Asigna el usuario al grupo correspondiente según su rol"""
        rol_to_group = {
            'admin': 'Administrador',
            'proveedor': 'Proveedor',
            'cliente': 'Cliente',
        }
        
        self.groups.clear()
        group_name = rol_to_group.get(self.rol, 'Cliente')
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    
    class Meta:
        db_table = 'login'


class Registro(models.Model):
    usuario = models.CharField(max_length=50, db_column='usuario')
    correo = models.EmailField(max_length=191, db_column='correo')
    contraseña = models.CharField(max_length=128, db_column='contraseña')
    telefono = models.CharField(max_length=15, db_column='telefono')

    def __str__(self):
        return f"{self.usuario} - {self.correo}"