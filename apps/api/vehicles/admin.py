from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'matricula', 'marca', 'modelo')
    search_fields = ('pk', 'matricula', 'marca', 'modelo')
    filter_horizontal = ('user',)
