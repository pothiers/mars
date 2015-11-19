import django_tables2 as tables

from .models import Slot

class SlotTable(tables.Table):
    class Meta:
        model = Slot
        fields = ("obsdate", "telescope", "propid_list")

