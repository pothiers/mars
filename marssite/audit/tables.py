import django_tables2 as tables

from .models import AuditRecord

class AuditRecordTable(tables.Table):
    class Meta:
        model = AuditRecord
        fields = ('instrument',
                  'notReceived',
                  'rejected',
                  'accepted' )



