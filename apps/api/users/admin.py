from django.contrib import admin

from .models import Profile, Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('pk', 'key', 'creado')
    search_fields = ('pk', 'key', 'creado')
    raw_id_fields = ('usuario',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bio', 'telefono', 'admin')
    search_fields = ('pk', 'bio', 'telefono', 'admin')
    raw_id_fields = ('usuario',)
