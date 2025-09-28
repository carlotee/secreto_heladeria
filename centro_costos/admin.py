from django.contrib import admin
from produccion.models import Producto
from gastos_comunes.models import GastosComunes
from reparto.models import Reparto

admin.site.site_header = "Secreto Heladeria - Admin"
admin.site.site_title = "Secreto Heladeria Admin"
admin.site.index_title = "Panel de Administración"

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(GastosComunes)
class GastosComunesAdmin(admin.ModelAdmin):
    list_display = ("nombre",)      
    search_fields = ("nombre",)     
    ordering = ("nombre",)          
    
@admin.register(Reparto)
class RepartoAdmin(admin.ModelAdmin):
    list_display = ("valor","fecha_reparto","fecha_ingreso","usuario")      
    search_fields = ("fecha_ingreso",)     
    ordering = ("fecha_ingreso",)          

