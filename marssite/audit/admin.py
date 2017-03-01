import datetime
from django.contrib import admin
from django.db.models import Count, Q, Sum, Case, When, IntegerField

from tada.models import Telescope,Instrument
from .models import AuditRecord

class ErrcodeFilter(admin.SimpleListFilter):
    title = 'errcode'
    parameter_name = 'errcode'
    
    def lookups(self, request, model_admin):
        qs = AuditRecord.objects.order_by('errcode').distinct('errcode')
        return [(rec.errcode, rec.errcode) for rec in qs]

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset
        else:
            return queryset.filter(errcode=self.value())

class InstrumFilter(admin.SimpleListFilter):
    title = 'instrument'
    parameter_name = 'instrument'
    
    def lookups(self, request, model_admin):
        qs = AuditRecord.objects.order_by('instrument').distinct('instrument')
        return [(rec.instrument, rec.instrument) for rec in qs]

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset
        else:
            return queryset.filter(instrument=self.value())

class TeleFilter(admin.SimpleListFilter):
    title = 'telescope'
    parameter_name = 'telescope'
    
    def lookups(self, request, model_admin):
        qs = AuditRecord.objects.order_by('telescope').distinct('telescope')
        return [(rec.telescope, rec.telescope) for rec in qs]

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset
        else:
            return queryset.filter(telescope=self.value())

    
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

def hide(modeladmin, request, queryset):
    queryset.update(hide=True)
hide.short_description = "Hide selected records"

def unhide(modeladmin, request, queryset):
    queryset.update(hide=False)
unhide.short_description = "Unhide selected records"

#!def clear_submit(modeladmin, request, queryset):
#!    queryset.update(submitted=None,
#!                    success=None,
#!                    archerr='',
#!                    errcode='none',
#!                    archfile='',
#!                    metadata=None,
#!                    )
#!clear_submit.short_description = "Clear archive submit related fields"
#!
#!def clear_error(modeladmin, request, queryset):
#!    queryset.update(archerr='',
#!                    errcode='none',
#!                    archfile='',
#!                    )
#!clear_error.short_description = "Clear archive error related fields"

@admin.register(AuditRecord)
#!class AuditRecordAdmin(admin.ModelAdmin):
#!    pass 
#!
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

    def display_fstop(obj):
        return obj.fstop
    display_fstop.short_description = "FStop"

    def display_srcpath(obj):
        maxlen=20
        strval = obj.srcpath
        if len(strval) > maxlen:
            return '...' + strval[-maxlen:]
        else:
            return strval
    display_srcpath.short_description = "SrcPath"
    
    def display_archerr(obj):
        maxlen=20
        sub='REASON: '
        strval = obj.archerr
        index = strval.find(sub)
        if index < 0:
            return strval
        else:
            return strval[len(sub) + index:]

    def display_updated(obj):
        return obj.updated.strftime('%x %X')
    display_updated.short_description = "Updated"

    def display_obsday(obj):
        if obj.obsday == None:
            # Should only happen after connection troubles
            return obj.obsday
        else:
            return obj.obsday.strftime('%x')
    display_obsday.short_description = "Obsday"

    def display_fstop_host(obj):
        return obj.fstop_host
    display_fstop_host.short_description = "host"
    
    
    list_display = (
        'staged',
        'hide',
        display_fstop, #'fstop',
        
        #display_updated, # makes sort by column stop working
        'updated',
        'success',
        display_obsday, #'obsday',
        'telescope',
        'instrument',
        #'narrow_srcpath',
        
        #display_srcpath, #'srcpath',
        'srcpath',
        display_archerr, #'archerr',
        'errcode',
        'archfile',
        #'metadata',
        #changed_fits_fields,
        'md5sum',
        display_fstop_host, #'fstop_host',
    )
 
    date_hierarchy = 'obsday'
    list_filter = ('success',
                   'hide',
                   #'obsday',
                   #! ObsdayListFilter,
                   'fstop',
                   #'errcode',
                   ErrcodeFilter,
                   'submitted',
                   #'instrument',
                   #'telescope',
                   InstrumFilter,
                   TeleFilter,
                   'staged')
    search_fields = ['telescope', 'instrument','srcpath', 'archerr', 'md5sum']
    actions = [stage,
               unstage,
               hide,
               unhide,
               #clear_submit,
               #clear_error,
    ]
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
        
