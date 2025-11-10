from django.contrib import admin
from django.utils import timezone
from .models import Costo, Producto
from .forms import CostoForm 


@admin.action(description="Eliminar costos seleccionados (borrado lógico)")
def eliminar_costos(modeladmin, request, queryset):
    """Acción personalizada para hacer borrado lógico de costos"""
    for costo in queryset:
        costo.deleted_at = timezone.now()
        costo.save()


@admin.register(Costo)
class CostoAdmin(admin.ModelAdmin):
    form = CostoForm  
    list_display = ("descripcion", "valor", "producto", "fecha", "deleted_at")
    search_fields = ("descripcion",)
    ordering = ("fecha",)
    actions = [eliminar_costos]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proveedor", "precio", "stock")
