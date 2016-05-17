from django.contrib import admin

from .models import SourceFile

class SourceFileAdmin(admin.ModelAdmin):
    list_display = (
        'md5sum',
        'obsday', 'telescope', 'instrument', 'srcpath',
        'recorded', 'submitted', 'success', 'archerr', 'archfile', 'metadata')
    
admin.site.register(SourceFile, SourceFileAdmin)
