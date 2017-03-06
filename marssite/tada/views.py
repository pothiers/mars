from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Site, Telescope, Instrument, FilePrefix
from .models import ObsType, ProcType, ProdType
from .models import RawKeywords, FilenameKeywords
from .models import IngestKeywords, IngestRecommendedKeywords
from .models import SupportKeywords, FloatKeywords, HdrFunc, TacInstrumentAlias
from .models import ErrorCode

# stilut=`curl 'http://localhost:8000/tada/'`
def prefix(request):
    qs = FilePrefix.objects.all().values('site__name',
                                         'telescope__name',
                                         'instrument__name',
                                         'prefix')
    return JsonResponse(list(qs), safe=False)

def obstype(request):
    qs = ObsType.objects.all().values('name','code')
    return JsonResponse(list(qs), safe=False)

def proctype(request):
    qs = ProcType.objects.all().values('name','code')
    return JsonResponse(list(qs), safe=False)

def prodtype(request):
    qs = ProdType.objects.all().values('name','code')
    return JsonResponse(list(qs), safe=False)

##############################################################################

def rawreq(request):
    qs = RawKeywords.objects.all().values('name','comment')
    return JsonResponse(list(qs), safe=False)

def filenamereq(request):
    qs = FilenameKeywords.objects.all().values('name','comment')
    return JsonResponse(list(qs), safe=False)

def ingestreq(request):
    qs = IngestKeywords.objects.all().values('name','comment')
    return JsonResponse(list(qs), safe=False)

def ingestrec(request):
    qs = IngestRecommendedKeywords.objects.all().values('name','comment')
    return JsonResponse(list(qs), safe=False)

def supportreq(request):
    qs = SupportKeywords.objects.all().values('name','comment')
    return JsonResponse(list(qs), safe=False)

def floatreq(request):
    qs = FloatKeywords.objects.all().values('name','comment')
    return JsonResponse(list(qs), safe=False)

##############################################################################

def hdrfuncs(request):
    qs = HdrFunc.objects.all().values('name',
                                      'documentation',
                                      'definition',
                                      'inkeywords',
                                      'outkeywords' )
    return JsonResponse(list(qs), safe=False)

def errcodes(request):
    qs = ErrorCode.objects.all().values('name','regexp')
    return JsonResponse(list(qs), safe=False)
