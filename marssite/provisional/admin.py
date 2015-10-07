from django.contrib import admin
from .models import Fitsname

# Register your models here.


class FitsnameAdmin(admin.ModelAdmin):
    list_display = ('id', 'source')
    
admin.site.register(Fitsname, FitsnameAdmin)

