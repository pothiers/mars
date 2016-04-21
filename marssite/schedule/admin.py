from django.contrib import admin
from .models import Slot, EmptySlot, SlotSet, Proposal

class PropInline(admin.TabularInline):
#class PropInline(admin.StackedInline):
    model = Slot.proposals.through

    #list_display = ('propid', 'pi_name')
    #filter_horizontal = ['proposal']
    extra=1
    raw_id_fields = ('proposal',)

    
@admin.register(EmptySlot)
class EmptySlotAdmin(admin.ModelAdmin):
    list_display = ('obsdate', 'telescope', 'instrument')
    list_filter = ['obsdate', 'telescope', 'instrument'] # right sidebar filter
    date_hierarchy = 'obsdate'


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('obsdate', 'telescope', 'instrument',
                    'propid_list', 'modified', 'frozen')
    list_filter = ['obsdate', 'telescope','instrument'] # right sidebar filtering
    filter_horizontal = ['proposals']
    date_hierarchy = 'obsdate'
    inlines = (PropInline,)
    exclude = ('proposals',)
    actions = ['freeze', 'unfreeze']
    list_editable = ['frozen',]

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
