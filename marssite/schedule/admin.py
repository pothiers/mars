from django.contrib import admin
from .models import Slot, SlotSet, Proposal

class PropInline(admin.TabularInline):
    model = Slot.proposals.through
    list_display = ('propid', 'pi_name')

    
@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    #!list_display = ('frozen', 'obsdate', 'telescope', 'propid')
    list_display = ('obsdate', 'telescope', 'propid_list', 'modified')
    list_filter = ['obsdate', 'telescope']
    filter_horizontal = ['proposals']
    date_hierarchy = 'obsdate'
    inlines = (PropInline,)
    exclude = ('proposals',)


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    fields = ('propid', 'title', ('pi_name', 'pi_affiliation'))
    list_display = ('propid', 'title', 'pi_name', 'pi_affiliation', 'modified')
    inlines = (PropInline,)

#@admin.register(SlotSet)    
class SlotSetAdmin(admin.ModelAdmin):
    list_display = ('xmlfile', 'comment')


#!admin.site.register(Slot, SlotAdmin)
#!admin.site.register(Proposal, ProposalAdmin)
#!admin.site.register(SlotSet, SlotSetAdmin)
