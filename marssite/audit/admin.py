import datetime
from django.contrib import admin
from django.db.models import Count, Q, Sum, Case, When, IntegerField

from .models import AuditRecord

# see: ~/sandbox/mars/env_mars/lib/python3.5/site-packages/django/contrib/admin/filters.py
class ObsdayListFilter(admin.SimpleListFilter):
    title = 'date observed'
    parameter_name = 'obsday'

    def lookups(self, request, model_admin):
        today = datetime.date.today()
        yesterday = (today - datetime.timedelta(days=1))


        tuples = [
            (None, 'Any date'),
            ('recent7', 'Past 7 days'),
            (str(yesterday.isoformat()), 'Yesterday'),
            (str(today.isoformat()), 'Today'),
        ]
        return tuples

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }    

    def queryset(self, request, queryset):
        #self.lookup_kwarg_since: str(today - datetime.timedelta(days=7)),
        #self.lookup_kwarg_until: str(tomorrow),
        today = datetime.date.today()
        recent7 = (today - datetime.timedelta(days=7))

        if self.value() == None:
            return queryset
        elif self.value() == 'recent7':
            return queryset.filter(obsday__gte=recent7, obsday__lt=today)
        else:
            return queryset.filter(obsday=self.value())


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

@admin.register(AuditRecord)
class AuditRecordAdmin(admin.ModelAdmin):

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
        'fstop',
        'obsday', 'telescope', 'instrument',
        #'narrow_srcpath',
        #display_srcpath,
        'srcpath',
        'success',
        'archerr',
        'updated',
        'submitted',
        'errcode',
        'archfile',
        #'metadata',
        #changed_fits_fields,
        'md5sum',
        'dome_host',
        'mountain_host',
        'valley_host',
    )
 
    date_hierarchy = 'obsday'
    list_filter = ('success',
                   #'obsday',
                   ObsdayListFilter,
                   'fstop',
                   'errcode',
                   'submitted',
                   'instrument',
                   'telescope',
                   'staged')
    search_fields = ['telescope', 'instrument','srcpath', 'archerr', 'md5sum']
    actions = [stage, unstage, clear_submit, clear_error]
    ordering = ['-updated',]

    #
    # This will NOT WORK because an admin queryset must return list of
    # MODEL INSSTANCES. Thefore this produces an exception:
    #   'dict' object has no attribute '_meta'
    #
    #!def get_queryset(self, request):
    #!    qs = super(AuditRecordAdmin, self).get_queryset(request)
    #!    group = ['obsday','instrument','telescope']
    #!    errcnts = qs.exclude(success=True).values(*group).annotate(
    #!        mtnjam=Sum(Case(When(success__isnull=True, then=1),
    #!                        output_field=IntegerField())),
    #!        valjam=Sum(Case(When(success=False, then=1),
    #!                        output_field=IntegerField()))
    #!    )
    #!    return errcnts
    
    class Media:
        css = {
            'all': ('audit/audit-admin.css',)
        }
        
