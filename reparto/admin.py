from django.contrib import admin
from .models import Cliente, Ventas, DetalleVenta, Usuario, Reparto


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('id',)


@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor_total', 'estado')
    search_fields = ('estado', 'valor_total')
    list_filter = ('estado',)
    ordering = ('-id',)


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor_unitario', 'ventas')
    search_fields = ('valor_unitario',)
    list_filter = ('ventas',)
    ordering = ('-id',)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('id',)


@admin.register(Reparto)
class RepartoAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor', 'fecha_reparto', 'fecha_ingreso', 'usuario')
    search_fields = ('valor',)
    list_filter = ('fecha_reparto', 'fecha_ingreso', 'usuario')
    ordering = ('-fecha_reparto',)
