from django.contrib import admin

from .models import Site, Telescope, Instrument#, FilePrefix


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass

@admin.register(Telescope)
class TelescopeAdmin(admin.ModelAdmin):
    pass

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    pass

#!@admin.register(FilePrefix)
#!class FilePrefixAdmin(admin.ModelAdmin):
#!   pass
#!    #!list_display = [
#!    #!    'site',
#!    #!    'telescope',
#!    #!    'instrument',
#!    #!    'prefix',
#!    #!]
