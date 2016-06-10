import datetime
from django.contrib import admin

from .models import SourceFile

# see: ~/sandbox/mars/env_mars/lib/python3.5/site-packages/django/contrib/admin/filters.py
class ObsdayListFilter(admin.SimpleListFilter):
    title = 'date observed'
    parameter_name = 'obsday'

    def lookups(self, request, model_admin):
        today = datetime.date.today()
        yesterday = (today - datetime.timedelta(days=1))
        return (
            (yesterday.isoformat(), 'Yesterday'),
            (today.isoformat(), 'Today'),
        )
    def queryset(self, request, queryset):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        if self.value() == 'Yesterday' :
            return queryset.filter(obsday__gte=yesterday, obsday__lt=today)
        if self.value() == 'Today' :
            return queryset.filter(obsday__gte=today)


def stage(modeladmin, request, queryset):
    queryset.update(staged=True)
stage.short_description = "Stage selected records for further actions"

def unstage(modeladmin, request, queryset):
    queryset.update(staged=False)
unstage.short_description = "Unstage selected records (no further actions)"

def clear_submit(modeladmin, request, queryset):
    queryset.update(submitted=None,
                    success=None,
                    archerr='',
                    errcode='none',
                    archfile='',
                    metadata=None,
                    )
clear_submit.short_description = "Clear archive submit related fields"

def clear_error(modeladmin, request, queryset):
    queryset.update(archerr='',
                    errcode='none',
                    archfile='',
                    )
clear_error.short_description = "Clear archive error related fields"

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
        'obsday', 'telescope', 'instrument',
        #'narrow_srcpath',
        #display_srcpath,
        'srcpath',
        'recorded',
        'submitted',
        'success',
        'errcode',
        'archerr',
        'archfile',
        #'metadata',
        #changed_fits_fields,
        'md5sum',
    )
 
    date_hierarchy = 'obsday'
    list_filter = ('success',
                   'obsday',
                   'errcode',
                   #ObsdayListFilter,
                   'submitted',
                   'instrument', 'telescope')
    search_fields = ['telescope', 'instrument','srcpath', 'archerr']
    actions = [stage, unstage, clear_submit, clear_error]
    ordering = ['-recorded',]

    class Media:
        css = {
            'all': ('audit/audit-admin.css',)
        }
        
