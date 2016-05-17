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

import datetime

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, render_to_response
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

from .models import SourceFile
#from .serializers import SubmittalSerializer, SourceFileSerializer
from .serializers import SourceFileSerializer
from .plotlib import hbarplot

from siap.models import VoiSiap

# curl http://localhost:8000/audit/ > ~/Downloads/list.json
#!class SubmittalList(generics.ListAPIView):
#!    model = Submittal
#!    queryset = Submittal.objects.all().all
#!    template_name = 'audit/submittal_list.html'
#!
#!    serializer_class = SubmittalSerializer
#!    paginate_by = 50
#!
#!class SubmittalDetail(generics.CreateAPIView):
#!    model = Submittal
#!    queryset = Submittal.objects.all()
#!    template_name = 'audit/submittal_detail.html'
#!    serializer_class = SubmittalSerializer
#!
#!
#!    #curl -H "Content-Type: application/json" -X POST -d '{"source":"xyz","archive":"xyz","status":"NA1", "metadata":"NA2"}' http://localhost:8000/audit/add
#!@csrf_exempt
#!@api_view(['POST'])
#!@parser_classes((JSONParser,))
#!def add_submit(request):
#!    """Add a SUBMIT record using JSON data."""
#!    #print('DBG: audit/add_submit. Request={}'.format(request))
#!    if request.method == 'POST':
#!        #!print('Raw Data: "{}"'.format(request.body))
#!        #!print('Parsed Data: "{}"'.format(request.data))
#!        #!print('source={}'.format(request.data['source']))
#!        obj = Submittal(**request.data)
#!        obj.save()
#!    return redirect(reverse('audit:submittal_list'))

##############################################################################
### Newer version
###

def demo_multibarhorizontalchart(request):
    """
    multibarhorizontalchart page
    """
    import random
    nb_element = 10
    xdata = range(nb_element)
    ydata = [i + random.randint(-10, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    extra_serie = {"tooltip": {"y_start": "", "y_end": " mins"}}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
    }

    charttype = "multiBarHorizontalChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('audit/multibarhorizontalchart.html', data)

# Just allow source path (which was the only key)
@csrf_exempt
def ORIG_source(request, format='yaml'):
    """Record list of source paths to be submitted for ingest.
EXAMPLE:    
    curl -d '/04202016/tele/img1.fits /04202016/tele/img2.fits' http://localhost:8000/audit/source/
    """
    if request.method == 'POST':
        for path in request.body.decode('utf-8').strip().split():
            print('DBG: source={}'.format(path))
            SourceFile.objects.update_or_create(
                srcpath=path,
                defaults=dict(recorded=timezone.now()
                ))
        qs = SourceFile.objects.all()
        return JsonResponse(serializers.serialize(format, qs), safe=False)
    else:
        return HttpResponse('ERROR: expected POST')

#curl -H "Content-Type: application/json" -X POST -d '{ "observations":
#   [ { "md5sum": "c89350d2f507a883bc6a3e9a6f418a11", "obsday": "2016-05-12", "telescope": "kp09m", "instrument": "whirc", "srcpath": "/data/20165012/foo1.fits" },
#     { "md5sum": "c89350d2f507a883bc6a3e9a6f418a12", "obsday": "2016-05-12", "telescope": "kp09m", "instrument": "whirc", "srcpath": "/data/20165012/foo2.fits" }
#   ] }' http://localhost:8000/audit/add
@csrf_exempt
@api_view(['POST'])
@parser_classes((JSONParser,))
def source(request, format='yaml'):
    """Record list of observations to be submitted for ingest.
EXAMPLE:    
    curl -H "Content-Type: application/json" -d @example-obs.json http://localhost:8000/audit/source/
    """
    if request.method == 'POST':
        addcnt=0
        preexisting = set()
        print('DBG: request.data={}'.format(request.data))
        for obs in request.data['observations']:
            print('DBG: obs={}'.format(obs))
            obj,created = SourceFile.objects.get_or_create(md5sum=obs['md5sum'],
                                                           defaults=obs)
            if created:
                addcnt+=1
            else:
                preexisting.add(obs['md5sum'])
        return HttpResponse('<p>Added {} audit records. {} already existed.\n'
                            .format(addcnt,len(preexisting)))
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

@csrf_exempt
@api_view(['POST'])
@parser_classes((JSONParser,))
def update(request, format='yaml'):
    """Update audit record"""
    if request.method == 'POST':    
        rdict = request.data.copy()
        md5 = rdict['md5sum']
        #rdict['metadata']['nothing_here'] = 'NA' # was: 0 (not a string)
        for k,v in rdict['metadata'].items():
            rdict['metadata'][k] = str(v) # required for HStoreField
        print('/audit/update: metadata={}'.format(rdict['metadata']))
        print('/audit/update: defaults={}'.format(rdict))

        initdefs = dict(obsday=str(datetime.date.today()),
                        telescope=rdict['telescope'],
                        instrument=rdict['instrument'],
                        srcpath=rdict['srcpath'],
                        recorded=rdict['recorded'],
                        )
        updatedefs = dict(submitted=rdict['submitted'],
                          archerr=rdict['archerr'],
                          archfile=rdict['archfile'],
                          metadata=rdict['metadata'],
                          )

        obj,created = SourceFile.objects.get_or_create(md5sum=md5,
                                                       defaults=initdefs)
        if created:
            pass # warning? Ingest attempt, but no previous dome record!

        for key,val in updatedefs.iteritems():
            setattr(obj, key, val)
        obj.save

    return HttpResponse ('Update finished. created={}, obj={}'
                         .format(created, obj))
            
def add_ingested():
    "Update Audit records using matching Ingest records from SIAP"
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

def refresh(request):
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
    Telescope = tables.Column()
    Instrument = tables.Column()
    ObsDay = tables.Column()
    notReceived = tables.Column()
    rejected =  tables.Column()
    accepted =  tables.Column()
    
    class Meta:
        attrs = {'class': 'progress'}


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

# See also: templates/audit/googlechart-hbar.html
def hbar_svg (request):
    #counts = dict() # counts[(tele,inst,day)] = (nosubmit,rejected,accepted)
    counts = get_counts()

    # Convert to XX format
    #! svg = plotlib.hbarplot(data)
    svg = hbarplot(counts)
    return HttpResponse (svg, content_type="Image/svg+xml")

def get_counts():
    """Return counts of files grouped by (instrument, telescope, obsday).
    RETURN: counts[] => (notsubmitted, rejected, accepted)
    """
    group = ['instrument','telescope','obsday']
    nosubmitqs = (SourceFile.objects.exclude(success__isnull=False)
                  .values(*group)
                  .annotate(total=Count('md5sum'))
                  .order_by(*group))
    nosubmit = dict([(tuple([ob[k] for k in group]), ob['total'])
                     for ob in nosubmitqs])

    rejectedqs = (SourceFile.objects.filter(success__exact=False)
                  .values(*group)
                  .annotate(total=Count('md5sum'))
                  .order_by(*group))
    rejected = dict([(tuple([ob[k] for k in group]),ob['total'])
                       for ob in rejectedqs])

    acceptedqs = (SourceFile.objects.filter(success__exact=True)
                  .values(*group)
                  .annotate(total=Count('md5sum'))
                  .order_by(*group))
    accepted = dict([(tuple([ob[k] for k in group]), ob['total'])
                       for ob in acceptedqs])
    sent = SourceFile.objects.count()
    assert (sent==(sum([n for n in nosubmit.values()])
                   + sum([n for n in rejected.values()])
                   + sum([n for n in accepted.values()])))

    counts = dict() # counts[(tele,inst,day)] = (nosubmit,rejected,accepted)
    for k in (SourceFile.objects.order_by('telescope','instrument','obsday')
              .distinct(*group).values_list(*group)):
        counts[k] = (nosubmit.get(k,0), rejected.get(k,0), accepted.get(k,0))
    return counts



def progress_count(request):
    """Counts we want (for each telescope+instrument):
sent::     Sent from dome
nosubmit:: Not received at Valley (in transit? lost?) 
rejected:: Archive rejected submission (not in DB but is in Inactive Queue)
accepted:: Archive accepted submission (should be in DB)

sent = nosubmit + (rejected + accepted))
"""
    add_ingested()
    progress = get_counts()
    instrums=[]
    for (tele,instr,day) in progress.keys():
        instrums.append(dict(Telescope=tele,
                             Instrument=instr,
                             ObsDay=day,
                             notReceived=progress[(tele,instr,day)][0],
                             rejected=progress[(tele,instr,day)][1],
                             accepted=progress[(tele,instr,day)][2]
                             ))
    #!print('instrums={}'.format(instrums))
    table = ProgressTable(instrums)
    c = {"instrum_table": table,
         "title": 'Progress of Submits from instruments',  }
    return render(request, 'audit/progress.html', c) 

def progress(request):
    """Bar chart of counts for each telescope+instrument:
#sent::     Sent from dome
nosubmit:: Not received at Valley (in transit? lost?) 
rejected:: Archive rejected submission (not in DB but is in Inactive Queue)
accepted:: Archive accepted submission (should be in DB)

sent = nosubmit + (rejected + accepted))
"""
    add_ingested()
    nosubmitqs = (SourceFile.objects.exclude(success__isnull=False)
                  .values('telescope','instrument')
                  .annotate(total=Count('md5sum'))
                  .order_by('instrument','telescope'))
    nosubmit = dict([((ob['telescope'],ob['instrument']),ob['total'])
                     for ob in nosubmitqs])

    rejectedqs = (SourceFile.objects.filter(success__exact=False)
                  .values('telescope','instrument')
                  .annotate(total=Count('md5sum'))
                  .order_by('instrument','telescope'))
    rejected = dict([((ob['telescope'],ob['instrument']),ob['total'])
                     for ob in rejectedqs])

    acceptedqs = (SourceFile.objects.filter(success__exact=True)
                  .values('telescope','instrument')
                  .annotate(total=Count('md5sum'))
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

    instrums = sorted(list(progress.keys()))
    xdata = ['{}:{}'.format(tele,inst) for tele,inst in sorted(progress.keys())]
    xdata = list(range(len(instrums)))

    ydata0 = [progress[k][0] for k in instrums]
    ydata1 = [progress[k][1] for k in instrums]
    ydata2 = [progress[k][2] for k in instrums]

    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " mins"},
        #"tooltips": True,
        #"showValues": True,
        #"tickFormat": None,
        #"style": 'stack',
        "y_axis_format": "",
        "x_axis_format": "",
    }

    chartdata = {
        'x': xdata,
        'name0': 'Not Received', 'y0': ydata0, 'extra0': extra_serie,
        'name1': 'Rejected',     'y1': ydata1, 'extra1': extra_serie,
        'name2': 'Accepted',     'y2': ydata2, 'extra2': extra_serie,
    }

    charttype = "multiBarHorizontalChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('audit/progress-bar-chart.html', data)
    
#!class SourceFileList(generics.ListAPIView):
#!    model = SourceFile
#!    queryset = SourceFile.objects.all()
#!    template_name = 'audit/submittal_list.html'
#!    serializer_class = SourceFileSerializer
#!    paginate_by = 50


class SourceFileList(ListView):
    model = SourceFile

    
