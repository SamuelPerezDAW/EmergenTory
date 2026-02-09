from django.contrib import admin

from .models import Checkitem, Checklist


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('pk', 'vehicle', 'created_at', 'updated_at')
    search_fields = ('pk', 'vehicle', 'created_at', 'updated_at')
    raw_id_fields = ('checkitem',)
    filter_horizontal = ('user',)


@admin.register(Checkitem)
class CheckItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'active')
    search_fields = ('pk', 'name', 'active')
