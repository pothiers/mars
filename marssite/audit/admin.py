from django.contrib import admin

from .models import SourceFile


def stage(modeladmin, request, queryset):
    queryset.update(staged=True)
stage.short_description = "Stage selected records for further actions"

def unstage(modeladmin, request, queryset):
    queryset.update(staged=False)
unstage.short_description = "Unstage selected records (no further actions)"

@admin.register(SourceFile)
class SourceFileAdmin(admin.ModelAdmin):
    def changed_fits_fields(obj):
        if obj.metadata == None:
            return ''
        else:
            strval = ', '.join(list(obj.metadata.keys()))
            if len(strval) > 10:
                return strval[:10] + '...'
            else:
                return strval
    def display_srcpath(obj):
        maxlen=30
        strval = obj.srcpath
        if len(strval) > maxlen:
            return '...' + strval[-maxlen:]
        else:
            return strval

    
    list_display = (
        'staged',
        'md5sum',
        'obsday', 'telescope', 'instrument',
        #'narrow_srcpath',
        #display_srcpath,
        'srcpath',
        'recorded', 'submitted',
        'success',
        'archerr', 'archfile',
        #'metadata',
        changed_fits_fields,
    )
 
    date_hierarchy = 'obsday'
    list_filter = ('success', 'submitted', 'obsday', 'instrument', 'telescope')
    search_fields = ['telescope', 'instrument','srcpath', 'archerr']
    actions = [stage, unstage]

    class Media:
        css = {
            'all': ('audit/audit-admin.css',)
        }
        
