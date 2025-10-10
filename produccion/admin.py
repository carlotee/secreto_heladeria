from django.contrib import admin
from .models import Costo

@admin.register(Costo)
class CostoAdmin(admin.ModelAdmin):
    list_display = ("descripcion", "valor", "producto", "fecha")
    search_fields = ("descripcion",)
    ordering = ("fecha",)
    

