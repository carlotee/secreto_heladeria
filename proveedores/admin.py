from django.contrib import admin
from .models import Proveedor, Producto
<<<<<<< HEAD
from produccion.models import Costo  
=======
from produccion.models import Costo
>>>>>>> ad2bf0e890e817e649c9511ad21c9524ddb558fb

class CostoInline(admin.TabularInline):
    model = Costo
    extra = 0
    fields = ("descripcion", "valor")
    show_change_link = True


class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 0
    fields = ("nombre", "precio", "stock")
    show_change_link = True


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "telefono")  
    search_fields = ("nombre", "rut")
    ordering = ("nombre",)
    inlines = [ProductoInline]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proveedor", "precio", "stock")
    search_fields = ("nombre",)
    ordering = ("nombre",)
    inlines = [CostoInline]
