from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, TodayArchiveView, DayArchiveView, WeekArchiveView, MonthArchiveView, ArchiveIndexView, DetailView
from django.db.models import Value

from .forms import SlotSetForm
from .models import Slot, EmptySlot, Proposal, DefaultPropid
from .upload import handle_uploaded_file
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .serializers import SlotSerializer
from .tables import SlotTable

import logging
import json
import subprocess
from datetime import date, datetime, timedelta
import xml.etree.ElementTree as ET
import urllib.parse
import urllib.request
from collections import defaultdict

# instrument Mapping from Dave's NOAOPROP service to FITS header fields
sched2hdr= {
    # TAC           DMO
    # Schedule      Fits Header
    'ARCoIRIS':    'arcoiris',
    'CFIM+T2K':    'ccd_imager',
    'COSMOS':      'cosmos',
    'DECam':       'decam',
    'Goodman':     'goodman',
    'HDI':         'hdi',
    'KOSMOS':      'kosmos',
    'MOSA3':       'mosaic3', #!
    'NEWFIRM':     'newfirm',
    'OSIRIS':      'osiris',
    'SAM':         'sami',		# should be sami
    'SOI':         'soi',
    'Spartan':     'spartan',
    'WHIRC':       'whirc',
    ########################################
    #'ODI':        '(p)odi',		# not archived - remove
    #(None:        'goodman spectrograph'}	# goodman as above
    #(None:        'bench'}			# bench
    #(None:        'spartan ir camera'}	# spartan as above
}


def apply_tac_update(**query):
    """Update/add object unless it already exists and is FROZEN. """
    logging.debug('apply tac update for query={}'.format(query))
    params = urllib.parse.urlencode(query)
    logging.debug('DBG: query={}, params={}'.format(query, params))
    url=('http://www.noao.edu/noaoprop/schedule.mpl?{}'.format(params))
    logging.debug('DBG: url={}'.format(url))
    try:
        with urllib.request.urlopen(url, timeout=4) as f:
            tree = ET.parse(f)
            root = tree.getroot()
    except:
        logging.error('MARS: Error contacting TAC Schedule at "{}"'.format(url))
        return None
    slot_pids = defaultdict(set) # dict[slot] = [propid, ...]
    for proposal in root:
        telescope = proposal.get('telescope')
        instrument = sched2hdr.get(proposal.get('instrument'),None)
        if instrument == None:
            continue
        if telescope == None:
            continue
        instrument = instrument.lower()
        telescope = telescope.lower()
        if telescope not in Slot.telescopes:
            logging.warning('MARS: Telescope "{}" not one of: {}'
                            .format(telescope, Slot.telescopes))
            continue
        if instrument not in Slot.instruments:
            logging.warning('MARS: Instrument "{}" not one of: {}'
                            .format(instrument, Slot.instruments))
            continue
        #!obsdate = datetime.strptime(proposal.get('date'),'%Y-%m-%d').date()
        obsdate = proposal.get('date')
        propid = proposal.get('propid')
        slot, smade = Slot.objects.get_or_create(telescope=telescope,
                                                 instrument=instrument,
                                                 obsdate=obsdate)
        msg = 'slot={}'.format(slot)
        if smade:
            # did NOT exist
            logging.debug('ADDED: {}, propid="{}"'.format(msg,propid))
            slot_pids[slot].add(propid)                    
        else:
            if slot.frozen:
                # already existed but FROZEN
                logging.debug('IGNORED FROZEN: {}'.format(msg))
            else:
                # already existed and NOT FROZEN
                if propid in slot_pids[slot]:
                    continue
                
                slot_pids[slot].add(propid)                    
                logging.debug('NOT FROZEN: {}; propids={}'.format(msg, slot_pids[slot]))
    logging.debug('slot_pids={}'.format(slot_pids))
    return(slot_pids)
    
def update_from_noaoprop(**query):
    slot_pids = apply_tac_update(**query) # dict[slot] = [propid, ...]
    logging.debug('update_from_noaoprop({}); slot_pids={}'.format(query,slot_pids))
    logging.debug('Updating propid lists for {} slots:'.format(len(slot_pids)))
    for index,(slot,propids) in enumerate(slot_pids.items()):
        prop_list = [Proposal.objects.get_or_create(pk=propid)[0]
                     for propid in propids]
        logging.debug('UPDATED[{}]: {}={}'.format(index, slot, prop_list))
        slot.proposals = list(prop_list)
    #return redirect('/schedule/')
    return slot_pids # dict[obsdate:telescope] = set([propid, ...])

def update_date(request, day):
    slot_pids = update_from_noaoprop(date=day) 
    d1 = datetime.strptime(day, '%Y-%m-%d').date()
    d2 = d1 + timedelta(days=1)
    return HttpResponse('Slots updated for day ({})= {}'
                        .format(day, ', '.join([str(s) for s in slot_pids])),
                        content_type='text/plain')

def update_semester(request, semester):
    slot_pids = update_from_noaoprop(semester=semester)
    return HttpResponse('Slots updated for semester ({})= {}'
                        .format(semester, ', '.join([str(s) for s in slot_pids])),
                        content_type='text/plain')


def delete_schedule(request):
    slots = Slot.objects.all().delete()
    slots = EmptySlot.objects.all().delete()
    return HttpResponse('DELETED', content_type='text/plain')
    
@api_view(['GET', 'POST'])
def upload_file(request):
    'Upload and XML file of schedule info and load into DB.'
    logging.debug('EXECUTING: views<schedule>:uploaded_file')
    if request.method == 'POST':
        form = SlotSetForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            load_schedule(request.FILES['xmlfile'])
            return HttpResponseRedirect('/schedule/') # on succses
    else:
        form = SlotSetForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('schedule/upload.html', c)    
    #!return render('schedule/upload.html', {'form': form})    


#@api_view(['GET'])
def list_full(request, limit=100):
    'List the schedule. This is the full schedule available to TADA.'
    serializer_class = SlotSerializer
    slots = Slot.objects.all()
    #slots = Slot.objects.all()[:limit]
    #table = SlotTable(Slot.objects.all())
    return render(request, 'schedule/list.html',
                  {
                      'title': 'All',
                      #'limit': limit,
                      'limit': 'NONE',
                      'slot_list': slots,
                      #'table': table,
                  })


@api_view(['GET'])
@list_route(methods=['get'])
def list_empty(request):
    """List slots (telescope,date) that were queried but for which there is 
no PROPID.  These should probably be filled."""
    slots = EmptySlot.objects.all()
    return render(request, 'schedule/list_empty.html',
                  {'limit': 'none', 'slot_list': slots})

##    request_serializer: ScheduleQuerySerializer
##    response_serializer: ScheduleSerializer
##    ---
##    omit_serializer: true

# EXAMPLE in bash:
#  propid=`curl 'http://127.0.0.1:8000/schedule/propid/ct13m/2014-12-25/'`
@api_view(['GET'])
def getpropid(request, telescope, instrument, date):
    """
    Retrieve a **propid** from the schedule given `telescope` and `date`.
    """
    # Default PROPID to use when we don't have one for tele, instrum
    serializer_class = SlotSerializer
    tele = telescope.lower()
    instrum = instrument.lower()
    ignore_default = ('1' == request.GET.get('ignore_default'))
    global_default = '!NEED-DEFAULT.{}.{}'.format(tele,instrum)
    try:
        slot = Slot.objects.get(obsdate=date,
                                telescope=tele,
                                instrument=instrum)
        proplist = slot.propids
        logging.debug('(mars) schedule/propid/{}/{}/{} = "{}"'
              .format(tele, instrum, date, proplist))
        return HttpResponse(proplist, content_type='text/plain')
    except:
        pass
    
    # MARS schedule slot not found...
    # ... try updating the date from TAC, and getting Slot again
    update_from_noaoprop(date=date) 
    try:
        slot = Slot.objects.get(obsdate=date, telescope=tele, instrument=instrum)
        proplist = slot.propids
        logging.debug('(post tac update) schedule/propid/{}/{}/{} = "{}"'
              .format(tele, instrum, date, proplist))
        return HttpResponse(proplist, content_type='text/plain')
    except:
        if ignore_default:
            logging.debug('(ignore default) schedule/propid/{}/{}/{} = "{}"'
                  .format(tele, instrum, date, 'NA'))
            return HttpResponse('NA', content_type='text/plain')            
    # ... use default
    try:
        logging.debug('Get default propid for tele={}, instrum={}'.format(tele,instrum))
        obj = DefaultPropid.objects.get(telescope=tele, instrument=instrum)
        proplist = obj.propids
    except Exception as ex:
        logging.debug('Need default propid for tele={}, instrum={}'
              .format(tele,instrum))
        proplist = [global_default]

    logging.debug('schedule/propid/{}/{}/{} = {}'.format(tele, instrum, date, proplist))
    return HttpResponse(proplist, content_type='text/plain')    
        

class SlotGet(generics.GenericAPIView, DetailView):
    """
    Retrieve a **propid** from the schedule given `telescope` and `date`.
    """
    serializer_class = SlotSerializer
    model = Slot
    template_name = 'schedule/slot_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['title'] = ('Schedule for Telescope ({tele}) on {date}'
                            .format(**self.kwargs))
        return context

    # HACK!!! Get list of 1 item. Template pulls out fields
    def get_queryset(self):
        return Slot.objects.filter(obsdate=self.kwargs['date'],
                                   telescope=self.kwargs['tele'])

    
def load_schedule(uploadedfile, maxsize=1e6):
    """Load schedule slots from XML file. Skip any slots (date,telescope)
that already have Propid values"""
    #!logging.debug('EXECUTING: load_schedule; name={}'.format(uploadedfile.name))
    if uploadedfile.size > maxsize:
        return None
    xmlstr = ''
    for line in uploadedfile:
        xmlstr += line.decode()
    root = ET.fromstring(xmlstr)
    #!tree = ET.parse(uploadedfile)
    created = root.get('created')
    begin = root.get('begindate')
    end = root.get('enddate')

    # kinda slow!  Perhaps because doing multi-queries + insert per slot.
    for proposal in root:
        obsdate = datetime.strptime(proposal.get('date'),'%Y-%m-%d').date()
        telescope = proposal.get('telescope')
        propid = proposal.get('propid')

        title=proposal.findtext('title')
        piname=proposal.findtext('piname')
        affiliation=proposal.findtext('affiliation')

        # Never overwrite existing Proposal or Slot
        dd=dict(pi_name=piname, pi_affiliation=affiliation, title=title)
        prop, pmade = Proposal.objects.get_or_create(pk=propid, defaults=dd)
        slot, smade = Slot.objects.get_or_create(telescope=telescope,
                                                 obsdate=obsdate)
        #!if pmade:
        #!    logging.debug('DBG-4.2a: created proposal record for propid={}'
        #!          .format(propid))
        #!else:
        #!    logging.debug('DBG-4.2b: Using previous proposal record for propid={}'
        #!          .format(propid))

        if smade:
            slot.proposals.add(prop)
            #!logging.debug('DBG-4.3a: created slot record for tele={}, date={}'
            #!      .format(telescope, obsdate))
        else:
            pass
            #!logging.debug('DBG-4.3b: Using previous slot record for tele={}, date={}'
            #!      .format(telescope, obsdate))
            
    return redirect('/schedule/')




#class SlotList(generics.ListAPIView, ArchiveIndexView):
class SlotList(APIView, ArchiveIndexView):
    "Display all scheduled observations."
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    #paginate_by = 200

class SlotDetail(APIView):
    "Retrieve, upate or deleted slot instance."
    def get_object(self, pk):
        try:
            return Slot.objects.get(pk=pk)
        except Slot.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        slot = self.get_object(pk)
        serializer = SlotSerializer(slot)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        slot = self.get_object(pk)
        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        slot = self.get_object(pk)
        slot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SlotList(generics.ListAPIView, ArchiveIndexView):
    "Display all scheduled observations."
    model = Slot
    date_field = 'obsdate'
    queryset = Slot.objects.all()
    allow_future = True
    template_name = 'schedule/slot_list.html'
    context_object_name = 'slot_list'

    serializer_class = SlotSerializer
    paginate_by = 200
    #!logging.debug('DBG: serializer={}'.format(repr(SlotSerializer())))

    def get_context_data(self, **kwargs):
        context = super(ArchiveIndexView, self).get_context_data(**kwargs)
        context['title'] = 'Full Schedule'
        return context

    


#class SlotTodayList(generics.ListAPIView, TodayArchiveView):
class SlotTodayList(generics.GenericAPIView,TodayArchiveView):
    "Display all scheduled observations for *TODAY*."
    queryset = Slot.objects.all()
    model = Slot
    date_field = 'obsdate'
    allow_future = True
    template_name = 'schedule/slot_list.html'
    context_object_name = 'slot_list'
    serializer_class = SlotSerializer

    def get_context_data(self, **kwargs):
        context = super(SlotTodayList, self).get_context_data(**kwargs)
        context['title'] = 'Schedule for today'
        return context

    def get_queryset(self, **kwargs):
        return super(TodayArchiveView, self).get_queryset(**kwargs)



class SlotMonthList(generics.GenericAPIView, MonthArchiveView):
    "Display all scheduled observations for the selected month."
    model = Slot
    date_field = 'obsdate'
    allow_future = True
    template_name = 'schedule/slot_list.html'
    context_object_name = 'slot_list'
    serializer_class = SlotSerializer
    ordering = 'obsdate'
    
    def get_queryset(self, **kwargs):
        return super(MonthArchiveView, self).get_queryset(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(SlotMonthList, self).get_context_data(**kwargs)
        context['title'] = ('Schedule for month: {}/{}'
                            .format(self.kwargs['month'],
                                    self.kwargs['year'] ))
        return context
    
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    paginate_by = 100
    serializer_class = SlotSerializer


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'upload': reverse('schedule:upload_file',
                          request=request, format=format),
        'empty': reverse('schedule:list_empty', request=request, format=format),
        'list': reverse('schedule:list', request=request, format=format),
    })

