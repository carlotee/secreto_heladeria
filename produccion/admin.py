from django.contrib import admin
from .models import Producto, Proveedor, OrdenCompra, DetalleCompra


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio')
    search_fields = ('nombre',)
    ordering = ('id',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('id',)


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor_total', 'estado', 'proveedor')
    search_fields = ('estado', 'valor_total')
    list_filter = ('estado', 'proveedor')
    ordering = ('-id',)


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor_unitario', 'cantidad_total', 'estado', 'producto')
    search_fields = ('estado', 'valor_unitario')
    list_filter = ('estado', 'producto')
    ordering = ('-id',)
