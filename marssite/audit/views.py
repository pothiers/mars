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

import dateutil.parser as dp
import re
import datetime
import logging
from pathlib import PurePath

import csv
from django.utils.timezone import make_aware, now
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db import connection
from django.db.models import Count, Q, Sum, Case, When, IntegerField
from django.template import Context, Template
from django.template.loader import get_template
from django.core.exceptions import ValidationError

import django_tables2 as tables
from django_tables2 import RequestConfig
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.decorators import  api_view,parser_classes

from .models import AuditRecord
from .tables import AggTable
#from .serializers import SubmittalSerializer, AuditRecordSerializer
from .serializers import AuditRecordSerializer
#!from .plotlib import hbarplot
import audit.errcodes as ec

from schedule.models import Slot
from natica.models import Site,Telescope,Instrument

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
            #print('DBG: source={}'.format(path))
            AuditRecord.objects.update_or_create(
                srcpath=path,
                defaults=dict(updated=now()
                ))
        qs = AuditRecord.objects.all()
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
    """Record list of observations to be submitted for ingest. Intended to be 
done from dome for all files.
EXAMPLE:    
    curl -H "Content-Type: application/json" -d @example-obs.json http://localhost:8000/audit/source/
    """
    if request.method == 'POST':
        addcnt=0 
        errcnt=0 
        preexisting = set()
        if 'observations' not in request.data:
            logging.error(('data in POST to audit/source does not contain'
                           ' "observations"; {}')
                          .format(list(request.data)))

        logging.debug('DBG-audit/source: request.data.observations={}'
              .format(list(request.data['observations'])))
        for obs in request.data['observations']:
            auditrec = dict(md5sum = obs['md5sum'],
                            obsday = obs['obsday'],
                            telescope = Telescope.objects.get(
                                pk=obs['telescope']),
                            instrument = Instrument.objects.get(
                                pk=obs['instrument']),
                            srcpath = obs['srcpath'],
                            fstop_host = obs.get('dome_host','<dome-host>'),
                            )

            ar = AuditRecord(**auditrec)
            try:
                ar.full_clean()
            except ValidationError as e:
                errcnt += 1
                logging.warning((
                    'Invalid JSON data passed to {url}. '
                    + 'Ignoring record for key {md5} and trying rest.; {valerr}'
                ).format(url=reverse('audit:source'),
                         md5=obs.get('md5sum','UNKNOWN'),
                         valerr=e.message_dict
                ))
                continue
            #! print('DBG: obs={}'.format(obs))
            obj,created = AuditRecord.objects.get_or_create(
                md5sum=obs['md5sum'],
                defaults=auditrec)
            if created:
                addcnt += 1
            else:
                preexisting.add((obj.md5sum, obj.srcpath))
        # END for
        if errcnt > 0:
            msg = ('ERROR: Added {} audit records. Got {} errors.'
                   ' {} already existed so ignored request to add.\n'
            ).format(addcnt, errcnt, len(preexisting))
            for m,s in preexisting:
                msg += '{}, {}\n'.format(m,s)
            logging.error(msg)
        else:
            msg = 'SUCCESS: added {} records'.format(addcnt)
        return HttpResponse(msg)
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
        logging.debug('body={}'.format(body))
        AuditRecord.objects.update_or_create(
            dict(source=src,
                 submitted=now(),
                 success=body.get('success',True),
                 archerr=body.get('archerr', ''),
                 archfile=body['archfile']))
        
        return JsonResponse(serializers.serialize(format, qs), safe=False)
    else:
        return HttpResponse('ERROR: expected POST')

exists_re = re.compile(r"has already been stored in the database")    

@csrf_exempt
def get_rejected_duplicates(request):
    """Get list of files (by checksum) that were not ingested because they were
already in the archive DB"""
    restr=r"has already been stored in the database"
    qs = (AuditRecord.objects.filter(success=False,  archerr__iregex=restr)
          .values('md5sum','srcpath'))
    return JsonResponse(list(qs), safe=False)
    #print('dupes={}'.format(list(serializers.serialize('xml',qs))))
    #return HttpResponse(list(serializers.serialize('xml',qs)))

@csrf_exempt
def get_rejected_missing(request):
    """Get list of files (by checksum) that were not ingested because they were
missing requires fields"""
    restr=r"is missing required metadata fields"
    qs = (AuditRecord.objects.filter(success=False,  archerr__iregex=restr)
          .values('md5sum','srcpath'))
    return JsonResponse(list(qs), safe=False)

def delete(request, md5sum):
    "Delete one audit record"
    AuditRecord.objects.filter(md5sum=md5sum).delete()
    return HttpResponse('Deleted audit record for md5sum: {}'.format(md5sum))


@api_view(['POST'])
@csrf_exempt
def update_fstop(request, md5sum, fstop, host):
    """Set the fstop (file-stop) tag to indicate a logical system location
    for the FITS file.  Intent is for fstop to be updated as FITS
    moves downstream from Dome to Archive. Since the location can be
    on one of serveral hosts, the host should also be given.
    """
    logging.debug('START update_fstop: fstop={}, host={}, md5sum={}'
          .format(fstop, host, md5sum))

    machine = fstop.split(':')[0]
    defaults = dict(fstop=fstop,
                    fstop_host=host,
                    updated=now(),
                    )
    obj, created = AuditRecord.objects.update_or_create(md5sum=md5sum,
                                                        defaults=defaults)
    logging.debug('END update_fstop: obsday={}, md5sum={}, defaults={}, created={}'
          .format(obj.obsday, md5sum, defaults, created))
    return HttpResponse('Updated FSTOP; {}'.format(md5sum))
    

def re_audit(request, orig_md5sum, new_md5sum):
    """Replace previous audit record with new (initialized) one."""
    try:
        obj = AuditRecord.objects.get(pk=orig_md5sum)
    except:
        return HttpResponse('Audit record for md5sum {} does not exist. Ignored'
                            .format(orig_md5sum))
    auditrec = dict(md5sum = new_md5sum,
                    obsday = obj.obsday,
                    telescope = obj.telescope,
                    instrument = obj.instrument,
                    srcpath = obj.srcpath,
                    fstop_host = obj.fstop_host,
    )
    ar = AuditRecord(**auditrec)
    ar.save()
    AuditRecord.objects.filter(md5sum=orig_md5sum).delete()
    
    return HttpResponse('Replaced audit record {} with {}'
                        .format(orig_md5sum, new_md5sum))
    

@csrf_exempt
@api_view(['POST'])
@parser_classes((JSONParser,))
def update(request, format='yaml'):
    """Update audit record"""
    if request.method == 'POST':  
        all = set([f.name for f in AuditRecord._meta.get_fields()])
        rdict = request.data.copy()
        rdict['telescope'] = Telescope.objects.get(pk=rdict['telescope'])
        rdict['instrument'] = Instrument.objects.get(pk=rdict['instrument'])

        logging.debug('uDBG-1')
        logging.debug('uDBG-rdict={}'.format(rdict))
        
        md5 = rdict['md5sum']
        #!try:
        #!    obj = AuditRecord.objects.get(md5)
        #!except:
        #!    return HttpResponse('Audit record for md5sum'
        #!                        '={} does not exist. Ignored'
        #!                        .format(md5))
        
        #rdict['metadata']['nothing_here'] = 'NA' # was: 0 (not a string)
        
        #!for k,v in rdict['metadata'].items():
        #!    rdict['metadata'][k] = str(v) # required for HStoreField
        #! print('/audit/update: defaults={}'.format(rdict)) 
        fstop = 'archive' if rdict['success']==True else 'valley:cache'
        #!initdefs = dict(obsday=rdict.get('obsday',now().date()),
        #!                telescope=tobj,
        #!                instrument=iobj,
        #!                srcpath=rdict['srcpath'] )
        #!newdefs = dict(obsday=rdict.get('obsday',now().date()),
        #!               telescope=tobj,
        #!               instrument=iobj,
        #!               srcpath=rdict['srcpath'],
        #!               #
        #!               submitted=make_aware(dp.parse(rdict['submitted'])),
        #!               success=rdict['success'],
        #!               fstop=fstop,
        #!               errcode=ec.errcode(rdict['archerr']), # rdict['errcode'],
        #!               archerr=rdict['archerr'],
        #!               archfile=rdict['archfile'],
        #!               #!metadata=rdict['metadata'],
        #!               updated=make_aware(dp.parse(rdict['updated'])) )
        logging.debug('uDBG-2')
        # Create new DB values from request dictionary
        newdefs = dict()
        for k in all & rdict.keys() - {'md5sum'}:
            newdefs[k] = rdict[k]
        newdefs['fstop'] = 'archive' if rdict.get('success','NA')==True \
                           else 'valley:cache'
        if 'submitted' in rdict:
            newdefs['submitted']=make_aware(dp.parse(rdict['submitted']))
        if 'archerr' in rdict:
            newdefs['errcode']=ec.errcode(rdict['archerr'])
        if 'updated' in rdict:
            newdefs['updated']=make_aware(dp.parse(rdict['updated']))
            
        logging.debug('uDBG-newdefs={}'.format(newdefs))
        try:
            obj,created = AuditRecord.objects.update_or_create(md5sum=md5,
                                                               defaults=newdefs)
        except Exception as err:
            return HttpResponseBadRequest(err)
            
        if created:
            logging.warning(('WARNING: Ingest requested, '
                   'but there was no previous dome record! '
                   'Adding: {} {}'.format(md5,rdict['srcpath'])))

        logging.debug('/audit/update/ saving obj={}, attrs={}'.format(obj.md5sum,dir(obj)))
        #!print('/audit/update/ saved obj={}'.format(obj))

        return HttpResponse('/audit/update/ DONE. created={}, obj={}'
                             .format(created, obj.md5sum))

def add_ingested():
    "Update Audit records using matching Ingest records from SIAP"
    cursor = connection.cursor()
    # Force material view refresh
    cursor.execute('SELECT * FROM refresh_voi_material_views()')
    sql = 'SELECT reference,dtacqnam FROM voi.siap WHERE dtacqnam = %s'
    for sf in AuditRecord.objects.all():
        qs = VoiSiap.objects.raw(sql,[sf.srcpath])
        #print('pairs={}'.format([(obj.reference, obj.dtacqnam) for obj in qs]))
        for obj in qs:
            AuditRecord.objects.filter(srcpath=obj.dtacqnam).update(
                success=True,
                arcerr = 'From SIAP',
                archfile=obj.reference)


def refresh(request):
    "Query Archive for all AuditRecords"
    add_ingested()
    return redirect('/admin/audit/sourcefile/')

def not_ingested(request):
    "Show source files that have not made it into the Archive"
    add_ingested()
    qs = AuditRecord.objects.filter(success=True)
    return render(request, 'audit/not_ingested.html', {"srcfiles": qs})

def failed_ingest(request):
    "Show source files that where submitted Archive but failed to ingest."
    add_ingested()
    qs = AuditRecord.objects.filter(success=False)
    return render(request, 'audit/failed_ingest.html', {"srcfiles": qs})

# The field 'uri' In the table edu_noao_nsa.data_product contains the actual
# file location.
def get_fits_location(reference, root='/net/archive/PAT/'):
    """RETURN: absolute path to FITS file
    reference:: Archive basename of FITS file"""
    cursor = connection.cursor()
    sql = ("SELECT dp.uri FROM voi.siap as vs, edu_noao_nsa.data_product as dp"
           " WHERE dp.data_product_id = vs.fits_data_product_id"
           " AND vs.reference= '{}'").format(reference)
    print('sql={}'.format(sql))
    cursor.execute(sql)
    uri = cursor.fetchone()
    if uri != None:
        ipath =  uri[0]
        #return str(PurePath(root, *PurePath(ipath).parts[2:]))
        return str(PurePath('/',*PurePath(ipath).parts[1:]))
        #return ipath
    return uri


def staged_archived_files(request):
    root = request.GET.get('root','/net/archive/')
    qs = AuditRecord.objects.filter(staged=True)
    arch_list = (obj  for obj in qs
                 if get_fits_location(obj.archfile, root=root))

    fitslist = [get_fits_location(obj.archfile, root=root) for obj in arch_list]
    print('DBG: fitslist({})={}'.format(len(fitslist), fitslist))
    #return JsonResponse(fitslist, safe=False)
    return HttpResponse(' '.join((f for f in fitslist if f)))

def staged_noarchived_files(request):
    root = request.GET.get('root','/net/archive/')
    qs = AuditRecord.objects.filter(staged=True)
    noarch_list = (obj  for obj in qs
                   if not get_fits_location(obj.archfile, root=root))
    cachelist = [obj.srcpath for obj in noarch_list]
    print('DBG: cachelist({})={}'.format(len(cachelist), cachelist))
    return HttpResponse(' '.join((f for f in cachelist if f)))

#!# PLACEHOLDER    
#!def matplotlib_bar_image (request, data):
#!    pos = arange(10)+ 2 
#!    
#!    barh(pos,(1,2,3,4,5,6,7,8,9,10),align = 'center')
#!    
#!    yticks(pos,('#hcsm','#ukmedlibs','#ImmunoChat','#HCLDR','#ICTD2015','#hpmglobal','#BRCA','#BCSM','#BTSM','#OTalk'))
#!    
#!    xlabel('Popularidad')
#!    ylabel('Hashtags')
#!    title('Gráfico de Hashtags')
#!    subplots_adjust(left=0.21)    
#!    buffer = io.BytesIO()
#!    canvas = pylab.get_current_fig_manager().canvas
#!    canvas.draw()
#!    graphIMG = PIL.Image.fromstring('RGB', canvas.get_width_height(), canvas.tostring_rgb())
#!    graphIMG.save(buffer, "PNG")
#!    pylab.close()
#!    return HttpResponse (buffer.getvalue(), content_type="Image/png")
#!
#!# See also: templates/audit/googlechart-hbar.html
#!def hbar_svg (request):
#!    #counts = dict() # counts[(tele,inst,day)] = (nosubmit,rejected,accepted)
#!    counts = get_counts()
#!
#!    # Convert to XX format
#!    #! svg = plotlib.hbarplot(data)
#!    svg = hbarplot(counts)
#!    return HttpResponse (svg, content_type="Image/svg+xml")

def get_counts():
    """Return counts of files grouped by (instrument, telescope, obsday).
    RETURN: counts[] => (notsubmitted, rejected, accepted)
    """
    group = ['instrument','telescope','obsday']
    nosubmitqs = (AuditRecord.objects.exclude(success__isnull=False)
                  .values(*group)
                  .annotate(total=Count('md5sum'))
                  .order_by(*group))
    nosubmit = dict([(tuple([ob[k] for k in group]), ob['total'])
                     for ob in nosubmitqs])

    rejectedqs = (AuditRecord.objects.filter(success__exact=False)
                  .values(*group)
                  .annotate(total=Count('md5sum'))
                  .order_by(*group))
    rejected = dict([(tuple([ob[k] for k in group]),ob['total'])
                       for ob in rejectedqs])

    acceptedqs = (AuditRecord.objects.filter(success__exact=True)
                  .values(*group)
                  .annotate(total=Count('md5sum'))
                  .order_by(*group))
    accepted = dict([(tuple([ob[k] for k in group]), ob['total'])
                       for ob in acceptedqs])
    sent = AuditRecord.objects.count()
    assert (sent==(sum([n for n in nosubmit.values()])
                   + sum([n for n in rejected.values()])
                   + sum([n for n in accepted.values()])))

    counts = dict() # counts[(tele,inst,day)] = (nosubmit,rejected,accepted)
    for k in (AuditRecord.objects.order_by('telescope','instrument','obsday')
              .distinct(*group).values_list(*group)):
        counts[k] = (nosubmit.get(k,0), rejected.get(k,0), accepted.get(k,0))
    return counts

# Q1: So this with materialized view so it can be under admin interface?
# A1: NO. Would make maintenance very complciated since mat-view outside
#     of MARS sphere.
# Q2: Overwrite admin get_queryset to get just error aggregates?
# A2: NO. Admin rows must represent OBJECTS.
def agg_domeday(request):
    """Find any aggregation (date,instrum,tele) with errors ordered by obsday.
    Intent is to drill down into these composit rows to find details of 
    an error.
    """
    #! from pprint import pprint
    group = ['obsday','instrument','telescope']
    ingesterrs = AuditRecord.objects.exclude(success=True)
    #!if ingesterrs.count() == 0:
    #!    table = AggTable(AuditRecords.objects.none())
    #!    return render(request, 'audit/agg.html',
    #!                  {'title': 'Aggregated error counts', 'agg': table})

    # Following works, but why bother seperating error types here?  Do
    # it on drill down instead. Because we cannot do OR or NEGATION in
    # URL querystring used in drill down!
    #
    errcnts = ingesterrs.values(*group).annotate(
        mtnjam=Sum(Case(When(success__isnull=True, then=1),
                        output_field=IntegerField())),
        valjam=Sum(Case(When(success=False, then=1),
                        output_field=IntegerField())),
        #!good=Sum(Case(When(success=True, then=1),
        #!                output_field=IntegerField())),
        total=Count('md5sum')
    ).order_by()
    #errcnts = ingesterrs.values(*group).annotate(jams=Count('md5sum'))
    #pprint(list(errcnts.order_by('obsday')))
    #table = AggTable(errcnts, order_by='obsday')
    table = AggTable(errcnts.order_by('-obsday'))
    RequestConfig(request, paginate={'per_page': 100}).configure(table)    
    return render(request, 'audit/agg.html',
                  {'title': 'Aggregated error counts', 'agg': table})

#!!# Eventually a replacement for Sean's CheckNight page
#!!def progress_count(request):
#!!    """Counts we want (for each telescope+instrument+obsday):
#!!sent::     Sent from dome
#!!nosubmit:: Not received at Valley (in transit? lost?) 
#!!rejected:: Archive rejected submission (not in DB but is in Inactive Queue)
#!!accepted:: Archive accepted submission (should be in DB)
#!!
#!!sent = nosubmit + (rejected + accepted))
#!!"""
#!!
#!!    #!add_ingested()
#!!    progress = get_counts() # (notsubmitted, rejected, accepted)
#!!    instrums=[]
#!!    for (instr,tele,day) in progress.keys():
#!!        try:
#!!            #obsdate=datetime.strptime(day,'%Y-%m-%d').date()
#!!            slot=Slot.objects.get(obsdate=day, telescope=tele, instrument=instr)
#!!            propids = slot.propids
#!!        except Slot.DoesNotExist:
#!!            propids=''
#!!        if day == None: continue
#!!        instrums.append(dict(Telescope=tele,
#!!                             Instrument=instr,
#!!                             ObsDay=day.isoformat(),
#!!                             dome=sum(progress[(instr,tele,day)]),
#!!                             notReceived=progress[(instr,tele,day)][0],
#!!                             rejected=progress[(instr,tele,day)][1],
#!!                             accepted=progress[(instr,tele,day)][2],
#!!                             Updated=now(),
#!!                             Propid = propids,
#!!                             ))
#!!    #!print('instrums={}'.format(instrums))
#!!    table = ProgressTable(sorted(instrums,
#!!                                 reverse=True, key=lambda d: d['ObsDay'] ))
#!!    c = {"instrum_table": table,
#!!         "title": 'faux DMO CheckNight Monitor',  }
#!!    return render(request, 'audit/progress.html', c) 
#!!
#!!def progress(request):
#!!    """Bar chart of counts for each telescope+instrument:
#!!#sent::     Sent from dome
#!!nosubmit:: Not received at Valley (in transit? lost?) 
#!!rejected:: Archive rejected submission (not in DB but is in Inactive Queue)
#!!accepted:: Archive accepted submission (should be in DB)
#!!
#!!sent = nosubmit + (rejected + accepted))
#!!"""
#!!    add_ingested()
#!!    nosubmitqs = (AuditRecord.objects.exclude(success__isnull=False)
#!!                  .values('telescope','instrument')
#!!                  .annotate(total=Count('md5sum'))
#!!                  .order_by('instrument','telescope'))
#!!    nosubmit = dict([((ob['telescope'],ob['instrument']),ob['total'])
#!!                     for ob in nosubmitqs])
#!!
#!!    rejectedqs = (AuditRecord.objects.filter(success__exact=False)
#!!                  .values('telescope','instrument')
#!!                  .annotate(total=Count('md5sum'))
#!!                  .order_by('instrument','telescope'))
#!!    rejected = dict([((ob['telescope'],ob['instrument']),ob['total'])
#!!                     for ob in rejectedqs])
#!!
#!!    acceptedqs = (AuditRecord.objects.filter(success__exact=True)
#!!                  .values('telescope','instrument')
#!!                  .annotate(total=Count('md5sum'))
#!!                  .order_by('instrument','telescope'))
#!!    accepted = dict([((ob['telescope'],ob['instrument']),ob['total'])
#!!                     for ob in acceptedqs])
#!!    sent = AuditRecord.objects.count()
#!!    assert (sent==(sum([n for n in nosubmit.values()])
#!!                   + sum([n for n in rejected.values()])
#!!                   + sum([n for n in accepted.values()])))
#!!    progress = dict() # progress[(tele,instr)] = (nosubmit,rejected,accepted)
#!!    for k in (AuditRecord.objects.order_by('telescope','instrument')
#!!              .distinct('telescope','instrument')
#!!              .values_list('telescope','instrument')):
#!!        progress[k] = (nosubmit.get(k,0), rejected.get(k,0), accepted.get(k,0))
#!!
#!!    instrums = sorted(list(progress.keys()))
#!!    xdata = ['{}:{}'.format(tele,inst) for tele,inst in sorted(progress.keys())]
#!!    xdata = list(range(len(instrums)))
#!!
#!!    ydata0 = [progress[k][0] for k in instrums]
#!!    ydata1 = [progress[k][1] for k in instrums]
#!!    ydata2 = [progress[k][2] for k in instrums]
#!!
#!!    extra_serie = {
#!!        "tooltip": {"y_start": "", "y_end": " mins"},
#!!        #"tooltips": True,
#!!        #"showValues": True,
#!!        #"tickFormat": None,
#!!        #"style": 'stack',
#!!        "y_axis_format": "",
#!!        "x_axis_format": "",
#!!    }
#!!
#!!    chartdata = {
#!!        'x': xdata,
#!!        'name0': 'Not Received', 'y0': ydata0, 'extra0': extra_serie,
#!!        'name1': 'Rejected',     'y1': ydata1, 'extra1': extra_serie,
#!!        'name2': 'Accepted',     'y2': ydata2, 'extra2': extra_serie,
#!!    }
#!!
#!!    charttype = "multiBarHorizontalChart"
#!!    data = {
#!!        'charttype': charttype,
#!!        'chartdata': chartdata
#!!    }
#!!    return render_to_response('audit/progress-bar-chart.html', data)
    
#!class AuditRecordList(generics.ListAPIView):
#!    model = AuditRecord
#!    queryset = AuditRecord.objects.all()
#!    template_name = 'audit/submittal_list.html'
#!    serializer_class = AuditRecordSerializer
#!    paginate_by = 50


class AuditRecordList(ListView):
    model = AuditRecord

    
def get_recent(request):
    #today = datetime.date.today()
    today = now()
    yesterday = (today - datetime.timedelta(days=1))

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="audit_recs.csv"'
    writer = csv.writer(response)
    writer.writerow(['STAGED', 'HIDE',
                     'FSTOP', 'UPDATED', 'SUCCESS',
                     'OBSDAY', 'TELESCOPE', 'INSTRUMENT',
                     'SRCPATH', 'ERRCODE', 'ARCHFILE'])
    for ar in (AuditRecord.objects
               .filter(updated__gte=yesterday).order_by('-updated')):
        writer.writerow([ar.staged, ar.hide,
                         ar.fstop, ar.updated, ar.success,
                         ar.obsday, ar.telescope, ar.instrument,
                         ar.srcpath, ar.errcode, ar.archfile,
                         ])
    return response
