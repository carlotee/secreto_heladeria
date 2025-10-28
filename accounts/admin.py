from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Registro

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Rol y número telefónico', {
            'fields': ('rol', 'numero',),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol y número telefónico', {
            'classes': ('wide',),
            'fields': ('rol', 'numero'),
        }),
    )


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'correo', 'telefono')
