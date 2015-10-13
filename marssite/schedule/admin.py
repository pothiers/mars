from django.contrib import admin
from .models import Slot


class SlotAdmin(admin.ModelAdmin):
    list_display = ('frozen', 'obsdate', 'telescope', 'propid')


admin.site.register(Slot, SlotAdmin)
