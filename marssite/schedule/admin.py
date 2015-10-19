from django.contrib import admin
from .models import Slot, SlotSet


class SlotAdmin(admin.ModelAdmin):
    list_display = ('frozen', 'obsdate', 'telescope', 'propid')

class SlotSetAdmin(admin.ModelAdmin):
    list_display = ('xmlfile', 'begin', 'end')


admin.site.register(Slot, SlotAdmin)
admin.site.register(SlotSet, SlotSetAdmin)
