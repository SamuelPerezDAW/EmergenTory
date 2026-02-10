from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'matricula', 'marca', 'modelo', 'categoria')
    search_fields = ('pk', 'matricula', 'marca', 'modelo', 'categoria')
    filter_horizontal = ('usuario',)
