from django.contrib import admin

admin.site.site_header = "Secreto Heladeria - Admin"
admin.site.site_title = "Secreto Heladeria Admin"
admin.site.index_title = "Panel de Administración"

from django.contrib import admin
from .models import Periodo, TipoCosto, Centro_Costos, Costo


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('año', 'mes')
    ordering = ('-año', '-mes')


@admin.register(TipoCosto)
class TipoCostoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Centro_Costos)
class CentroCostosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_costo', 'created_at', 'deleted_at')
    list_filter = ('tipo_costo',)
    search_fields = ('nombre',)


@admin.register(Costo)
class CostoAdmin(admin.ModelAdmin):
    list_display = ('descripcion','valor','tipo_costo', 'centro_costo', 'periodo')
    list_filter = ('tipo_costo', 'periodo')
    search_fields = ('descripcion',)
