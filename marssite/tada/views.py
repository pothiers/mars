from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Site, Telescope, Instrument, FilePrefix
from .models import ObsType, ProcType, ProdType


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

