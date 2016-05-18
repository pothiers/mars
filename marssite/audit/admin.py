from django.contrib import admin

from .models import SourceFile

@admin.register(SourceFile)
class SourceFileAdmin(admin.ModelAdmin):
    def changed_fits_fields(obj):
        return ', '.join(list(obj.metadata.keys()))
    
    list_display = (
        'md5sum',
        'obsday', 'telescope', 'instrument', 'srcpath',
        'recorded', 'submitted', 'success', 'archerr', 'archfile',
        #'metadata',
        changed_fits_fields,
    )
    
    date_hierarchy = 'obsday'
    list_filter = ('obsday', 'telescope', 'instrument')

    class Media:
        css = {
            'all': ('audit/audit-admin.css',)
        }
        
