from django.contrib import admin

from .models import Site, Telescope, Instrument, FilePrefix
from .models import ObsType, ProcType, ProdType
from .models import RawKeywords, FilenameKeywords
from .models import IngestKeywords, IngestRecommendedKeywords
from .models import SupportKeywords, FloatKeywords, HdrFunc, TacInstrumentAlias
from .models import ErrorCode


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass

@admin.register(Telescope)
class TelescopeAdmin(admin.ModelAdmin):
    pass

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name',)    


@admin.register(FilePrefix)
class FilePrefixAdmin(admin.ModelAdmin):
    list_display = ('site', 'telescope', 'instrument', 'prefix', 'comment')


@admin.register(ObsType)
class ObsTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(ProcType)
class ProcTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(ProdType)
class ProdTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(IngestRecommendedKeywords)
class IngestRecommendedKeywordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')


admin.site.register(RawKeywords)
admin.site.register(FilenameKeywords)
admin.site.register(IngestKeywords)
admin.site.register(SupportKeywords)
admin.site.register(FloatKeywords)

@admin.register(HdrFunc)
class HdrFuncAdmin(admin.ModelAdmin):
    list_display = ('name', 'documentation', 'inkeywords', 'outkeywords')

@admin.register(TacInstrumentAlias)
class TacInstrumentAliasAdmin(admin.ModelAdmin):
    list_display = ('tac','hdr')

@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ('name','regexp', 'shortdesc')
    
