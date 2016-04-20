from django.contrib import admin

from .models import Submittal, SourceFile

class SourceFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'when')
    
admin.site.register(SourceFile, SourceFileAdmin)
