from django.contrib import admin

from .models import MenuItem


@admin.register(MenuItem)
class Menu(admin.ModelAdmin):
    list_display = ('title', 'menu_name', 'parent', 'url', 'named_url')
    list_filter = ('menu_name',)
    search_fields = ('title',)
    ordering = ('title', 'id')
