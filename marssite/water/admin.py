from django.contrib import admin

from .models import FilePrefix

@admin.register(FilePrefix)
class FilePrefixAdmin(admin.ModelAdmin):
    list_display = [
        'site',
        'telescope',
        'instrument',
        'tacinst',
        'prefix',
    ]
