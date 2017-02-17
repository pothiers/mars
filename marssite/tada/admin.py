from django.contrib import admin

from .models import Site, Telescope, Instrument, FilePrefix
from .models import ObsType, ProcType, ProdType


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass

@admin.register(Telescope)
class TelescopeAdmin(admin.ModelAdmin):
    pass

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    pass

@admin.register(FilePrefix)
class FilePrefixAdmin(admin.ModelAdmin):
    pass

@admin.register(ObsType)
class ObsTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(ProcType)
class ProcTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(ProdType)
class ProdTypeAdmin(admin.ModelAdmin):
    pass
