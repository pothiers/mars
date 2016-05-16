import django_tables2 as tables

from .models import SourceFile

class SourceFileTable(tables.Table):
    class Meta:
        model = SourceFile
        fields = ('instrument',
                  'notReceived',
                  'rejected',
                  'accepted' )



