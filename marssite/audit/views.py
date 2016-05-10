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
#
# Graph using:
#  django-graphos-3;  bad documentation


from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.utils import timezone
from django.db import connection
from django.db.models import Count
from django.template import Context, Template
from django.template.loader import get_template

import django_tables2 as tables
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
        qs = VoiSiap.objects.raw(sql,[sf.srcpath])
        #print('pairs={}'.format([(obj.reference, obj.dtacqnam) for obj in qs]))
        for obj in qs:
            SourceFile.objects.filter(srcpath=obj.dtacqnam).update(
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

class ProgressTable(tables.Table):
    instrument = tables.Column()
    notReceived = tables.Column()
    rejected =  tables.Column()
    accepted =  tables.Column()
    


# PLACEHOLDER    
def matplotlib_bar_image (request, data):
    pos = arange(10)+ 2 
    
    barh(pos,(1,2,3,4,5,6,7,8,9,10),align = 'center')
    
    yticks(pos,('#hcsm','#ukmedlibs','#ImmunoChat','#HCLDR','#ICTD2015','#hpmglobal','#BRCA','#BCSM','#BTSM','#OTalk'))
    
    xlabel('Popularidad')
    ylabel('Hashtags')
    title('Gráfico de Hashtags')
    subplots_adjust(left=0.21)
    
    buffer = io.BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.fromstring('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    
    return HttpResponse (buffer.getvalue(), content_type="Image/png")

def progress_count(request):
    """Counts we want (for each telescope+instrument):
sent::     Sent from dome
nosubmit:: Not received at Valley (in transit? lost?) 
rejected:: Archive rejected submission (not in DB but is in Inactive Queue)
accepted:: Archive accepted submission (should be in DB)

sent = nosubmit + (rejected + accepted))
"""
    add_ingested()
    nosubmitqs = (SourceFile.objects.exclude(success__isnull=False)
                  .values('telescope','instrument')
                  .annotate(total=Count('srcpath'))
                  .order_by('instrument','telescope'))
    nosubmit = dict([((ob['telescope'],ob['instrument']),ob['total'])
                     for ob in nosubmitqs])

    rejectedqs = (SourceFile.objects.filter(success__exact=False)
                  .values('telescope','instrument')
                  .annotate(total=Count('srcpath'))
                  .order_by('instrument','telescope'))
    rejected = dict([((ob['telescope'],ob['instrument']),ob['total'])
                     for ob in rejectedqs])

    acceptedqs = (SourceFile.objects.filter(success__exact=True)
                  .values('telescope','instrument')
                  .annotate(total=Count('srcpath'))
                  .order_by('instrument','telescope'))
    accepted = dict([((ob['telescope'],ob['instrument']),ob['total'])
                     for ob in acceptedqs])
    sent = SourceFile.objects.count()
    assert (sent==(sum([n for n in nosubmit.values()])
                   + sum([n for n in rejected.values()])
                   + sum([n for n in accepted.values()])))
    progress = dict() # progress[(tele,instr)] = (nosubmit,rejected,accepted)
    for k in (SourceFile.objects.order_by('telescope','instrument')
              .distinct('telescope','instrument')
              .values_list('telescope','instrument')):
        progress[k] = (nosubmit.get(k,0), rejected.get(k,0), accepted.get(k,0))
    #return JsonResponse(serializers.serialize(format, qs), safe=False)
    #return HttpResponse('counts: {}'.format(progress))
    instrums=[]
    for (tele,instr) in progress.keys():
        instrums.append(dict(instrument='{}-{}'.format(tele,instr),
                             notReceived=progress[(tele,instr)][0],
                             rejected=progress[(tele,instr)][1],
                             accepteded=progress[(tele,instr)][2]
                             ))
    print('instrums={}'.format(instrums))
    table = ProgressTable(instrums)
    c = {"instrum_table": table,
         "title": 'Progress of Submits from instruments',  }
    return render(request, 'audit/progress.html', c) 

#!class SourceFileList(generics.ListAPIView):
#!    model = SourceFile
#!    queryset = SourceFile.objects.all()
#!    template_name = 'audit/submittal_list.html'
#!    serializer_class = SourceFileSerializer
#!    paginate_by = 50


class SourceFileList(ListView):
    model = SourceFile

    
