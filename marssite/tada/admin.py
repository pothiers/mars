from django.contrib import admin

from .models import Site, Telescope, Instrument

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass

@admin.register(Telescope)
class TelescopeAdmin(admin.ModelAdmin):
    pass

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    pass

