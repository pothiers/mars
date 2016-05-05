from django.contrib import admin

from .models import Submittal, SourceFile

class SourceFileAdmin(admin.ModelAdmin):
    list_display = (
        'telescope', 'instrument', 'srcpath',
        'recorded', 'submitted', 'success', 'archerr', 'archfile')
    
admin.site.register(SourceFile, SourceFileAdmin)
