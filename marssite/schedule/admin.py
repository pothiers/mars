from django.contrib import admin
from .models import Slot, EmptySlot, SlotSet, Proposal, DefaultPropid

class PropInline(admin.TabularInline):
#class PropInline(admin.StackedInline):
    model = Slot.proposals.through

    #list_display = ('propid', 'pi_name')
    #filter_horizontal = ['proposal']
    extra=1
    raw_id_fields = ('proposal',)

    
#!@admin.register(EmptySlot)
#!class EmptySlotAdmin(admin.ModelAdmin):
#!    list_display = ('obsdate', 'telescope', 'instrument')
#!    list_filter = ['obsdate', 'telescope', 'instrument'] # right sidebar filter
#!    date_hierarchy = 'obsdate'

@admin.register(DefaultPropid)
class DefaultPropidAdmin(admin.ModelAdmin):
    list_display = ('telescope', 'instrument', 'propids')
    

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('obsdate', 'telescope', 'instrument',
                    'propid_list', 'modified', 'frozen', 'split')
    list_filter = ['frozen', 'split', 'obsdate', 'instrument', 'telescope']
    filter_horizontal = ['proposals']
    date_hierarchy = 'obsdate'
    inlines = (PropInline,)
    exclude = ('proposals',)
    actions = ['freeze', 'unfreeze', 'split', 'unsplit', 'maybesplit']
    list_editable = ['frozen','split']

    def freeze(self, request, queryset):
        count = queryset.update(frozen=True)
        msg = "1 slot was" if count == 1 else '%s slots were'%count
        self.message_user(request, '%s frozen' % msg)
    freeze.short_description = 'Disallow bulk updates from changing slot'
    
    def unfreeze(self, request, queryset):
        count = queryset.update(frozen=False)
        msg = "1 slot was" if count == 1 else '%s slots were'%count
        self.message_user(request, '%s thawed' % msg)
    unfreeze.short_description = 'Allow bulk updates to change slot'

    def split(self, request, queryset):
        count = queryset.update(split=True)
        msg = "1 slot was" if count == 1 else '%s slots were'%count
        self.message_user(request, '%s set to use Split Night' % msg)
    split.short_description = 'Set to use Split Night'

    def unsplit(self, request, queryset):
        count = queryset.update(split=False)
        msg = "1 slot was" if count == 1 else '%s slots were'%count
        self.message_user(request, '%s set to NOT use Split Night' % msg)
    unsplit.short_description = 'Set to NOT use Split Night'

#!    def maybesplit(self, request, queryset):
#!        queryset.update(split=False)
#!        Slot.objects.all()\
#!                    .annotate(c=Count('proposals')).filter(c__gt=1)\
#!                    .update(split=True)
#!        count = queryset.update(split=True)
#!        msg = "1 slot was" if count == 1 else '%s slots were'%count
#!        self.message_user(request, '%s set to use Split Night' % msg)
#!    maybesplit.short_description = ('Set to use Split Night IFF'
#!                                    ' slot has more than 1 propid right now.')
    
    def save_model(self, request, obj, form, change):
        obj.frozen = True
        obj.save()

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    #fields = ('propid', 'title', ('pi_name', 'pi_affiliation'))
    #list_display = ('propid', 'title', 'pi_name', 'pi_affiliation', 'modified')
    list_display = ('propid','modified')
    #!inlines = (PropInline,)

#@admin.register(SlotSet)    
class SlotSetAdmin(admin.ModelAdmin):
    list_display = ('xmlfile', 'comment')


#!admin.site.register(Slot, SlotAdmin)
#!admin.site.register(Proposal, ProposalAdmin)
#!admin.site.register(SlotSet, SlotSetAdmin)
