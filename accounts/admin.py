from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Registro

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'numero', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'correo', 'telefono')
