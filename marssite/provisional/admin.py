from django.contrib import admin
from .models import Fitsname


class FitsnameAdmin(admin.ModelAdmin):
    list_display = ('id', 'source')
    
admin.site.register(Fitsname, FitsnameAdmin)

