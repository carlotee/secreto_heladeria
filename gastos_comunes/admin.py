from django.contrib import admin
from .models import GastosComunes, BoletaGC


class GastosComunesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('id',)


class BoletaGCAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor', 'fecha', 'gastosComunes')
    search_fields = ('valor',)
    list_filter = ('fecha', 'gastosComunes')
    ordering = ('-fecha',)


# Registro manual (sin duplicación)
admin.site.register(GastosComunes, GastosComunesAdmin)
admin.site.register(BoletaGC, BoletaGCAdmin)
