from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at', 'deleted_at')
    ordering = ('id',)
