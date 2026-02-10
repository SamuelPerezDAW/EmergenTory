from django.contrib import admin

from .models import Checkitem, Checklist


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('pk', 'vehiculo', 'creado', 'actualizado')
    search_fields = ('pk', 'vehiculo', 'creado', 'actualizado')
    raw_id_fields = ('vehiculo',)
    filter_horizontal = ('usuario',)


@admin.register(Checkitem)
class CheckItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'activo')
    search_fields = ('pk', 'nombre', 'activo')
