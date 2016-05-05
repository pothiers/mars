# Use to insure all files from domes make it into Archive.
# Files from dome is identified by combination of:
#   telescope
#   instrument
#   dome host
#   full path of FITS (on dome)
#
# If a file doesn't make it into the archive, we want to know why.
# Bad header? (missing values, fails TADA validation test)
# Archived rejected it? (error message?)
# Didn't make it to Valley? Didn't make it to Mountain?

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.utils import timezone
from django.db import connection

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.decorators import  api_view,parser_classes

from .models import Submittal, SourceFile
from .serializers import SubmittalSerializer, SourceFileSerializer

from siap.models import VoiSiap

# curl http://localhost:8000/audit/ > ~/Downloads/list.json
class SubmittalList(generics.ListAPIView):
    model = Submittal
    queryset = Submittal.objects.all().all
    template_name = 'audit/submittal_list.html'

    serializer_class = SubmittalSerializer
    paginate_by = 50

class SubmittalDetail(generics.CreateAPIView):
    model = Submittal
    queryset = Submittal.objects.all()
    template_name = 'audit/submittal_detail.html'
    serializer_class = SubmittalSerializer


    #curl -H "Content-Type: application/json" -X POST -d '{"source":"xyz","archive":"xyz","status":"NA1", "metadata":"NA2"}' http://localhost:8000/audit/add
@csrf_exempt
@api_view(['POST'])
@parser_classes((JSONParser,))
def add_submit(request):
    """Add a SUBMIT record using JSON data."""
    #print('DBG: audit/add_submit. Request={}'.format(request))
    if request.method == 'POST':
        #!print('Raw Data: "{}"'.format(request.body))
        #!print('Parsed Data: "{}"'.format(request.data))
        #!print('source={}'.format(request.data['source']))
        obj = Submittal(**request.data)
        obj.save()
    return redirect(reverse('audit:submittal_list'))

##############################################################################
### Newer version
###

@csrf_exempt
def source(request, format='yaml'):
    """Record list of source paths to be submitted for ingest.
EXAMPLE:    
    curl -d '/04202016/tele/img1.fits /04202016/tele/img2.fits' http://localhost:8000/audit/source/
    """


    if request.method == 'POST':
        for path in request.body.decode('utf-8').strip().split():
            print('DBG: source={}'.format(path))
            SourceFile.objects.update_or_create(
                source=path,
                defaults=dict(recorded=timezone.now()
                ))
        qs = SourceFile.objects.all()
        return JsonResponse(serializers.serialize(format, qs), safe=False)
    else:
        return HttpResponse('ERROR: expected POST')

@csrf_exempt
def submit(request, format='yaml'):
    """Record results of Archive ingest submittal.
EXAMPLE:    
    curl -H "Content-Type: application/json" -X POST \
      -d '{"source":"/a/b.fits","archfile":"xyz"}' \
       http://localhost:8000/audit/source/
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        print('body={}'.format(body))
        SourceFile.objects.update_or_create(
            dict(source=src,
                 submitted=timezone.now(),
                 success=body.get('success',True),
                 archerr=body.get('archerr', ''),
                 archfile=body['archfile']))
        
        return JsonResponse(serializers.serialize(format, qs), safe=False)
    else:
        return HttpResponse('ERROR: expected POST')


def add_ingested():    
    cursor = connection.cursor()
    # Force material view refresh
    cursor.execute('SELECT * FROM refresh_voi_material_views()')
    sql = 'SELECT reference,dtacqnam FROM voi.siap WHERE dtacqnam = %s'
    for sf in SourceFile.objects.all():
        qs = VoiSiap.objects.raw(sql,[sf.source])
        #print('pairs={}'.format([(obj.reference, obj.dtacqnam) for obj in qs]))
        for obj in qs:
            SourceFile.objects.filter(source=obj.dtacqnam).update(
                success=True,
                archfile=obj.reference)

def update(request):
    "Query Archive for all SourceFiles"
    add_ingested()
    return redirect('/admin/audit/sourcefile/')

def not_ingested(request):
    "Show source files that have not made it into the Archive"
    add_ingested()
    qs = SourceFile.objects.filter(success=True)
    return render(request, 'audit/not_ingested.html', {"srcfiles": qs})

def failed_ingest(request):
    "Show source files that where submitted Archive but failed to ingest."
    add_ingested()
    qs = SourceFile.objects.filter(success=False)
    return render(request, 'audit/failed_ingest.html', {"srcfiles": qs})

def progress_count(request):
    add_ingested()
    qs = SourceFile.objects.filter(success=False)    

#!class SourceFilelList(generics.ListAPIView):
#!    model = SourceFile
#!    queryset = SourceFile.objects.all()
#!    template_name = 'audit/submittal_list.html'
#!    serializer_class = SourceFileSerializer
#!    paginate_by = 50


class SourceFilelList(ListView):
    model = SourceFile

    
