from django.contrib import admin

from .models import Profile, Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('pk', 'key', 'created_at')
    search_fields = ('pk', 'key', 'created_at')
    raw_id_fields = ('user',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bio', 'phone_number', 'admin', 'user')
    search_fields = ('pk', 'bio', 'phone_number', 'admin', 'user')
    raw_id_fields = ('user',)
