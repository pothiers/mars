from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, TodayArchiveView, DayArchiveView, WeekArchiveView, MonthArchiveView, ArchiveIndexView, DetailView

from .forms import SlotSetForm
from .models import Slot, EmptySlot, Proposal
from .upload import handle_uploaded_file
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .serializers import SlotSerializer

import json
import subprocess
from datetime import date, datetime, timedelta as td
import xml.etree.ElementTree as ET



def delete_schedule(request):
    slots = Slot.objects.all().delete()
    slots = EmptySlot.objects.all().delete()
    return redirect('/schedule/')
    
@api_view(['GET', 'POST'])
def upload_file(request):
    'Upload and XML file of schedule info and load into DB.'
    print('EXECUTING: views<schedule>:uploaded_file')
    if request.method == 'POST':
        print('DBG-2')
        form = SlotSetForm(request.POST, request.FILES)
        if form.is_valid():
            print('DBG-2.1')
            # file is saved
            form.save()
            load_schedule(request.FILES['xmlfile'])
            return HttpResponseRedirect('/schedule/') # on success
    else:
        print('DBG-3')
        form = SlotSetForm()
    print('DBG-4')
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('schedule/upload.html', c)    
    #!return render('schedule/upload.html', {'form': form})    

3

@api_view(['GET'])
def list(request, limit=100):
    'List the schedule. This is the full schedule available to TADA.'
    serializer_class = SlotSerializer
    slots = Slot.objects.all()
    #slots = Slot.objects.all()[:limit]
    return render(request,
                  'schedule/list.html',
                  RequestContext(request, {
                      'title': 'All',
                      #'limit': limit,
                      'limit': 'NONE',
                      'slot_list': slots,
                  })
                  )

@api_view(['GET'])
@list_route(methods=['get'])
def list_empty(request):
    """List slots (telescope,date) that were queried but for which there is 
no PROPID.  These should probably be filled."""
    slots = EmptySlot.objects.all()
    return render(request,
                  'schedule/list_empty.html',
                  RequestContext(request, {
                                 'limit': 'none',
                                 'slot_list': slots,
                  })
                  )

#!def list_day(request, date, limit=1000):
#!    slots = Slot.objects.filter(obsdate=date)[:limit]
#!    return render(request,
#!                  'schedule/list.html',
#!                  RequestContext(request, {
#!                      'title': 'Day: {}'.format(date),
#!                      'limit': limit,
#!                      'slot_list': slots,
#!                  })
#!                  )


##    request_serializer: ScheduleQuerySerializer
##    response_serializer: ScheduleSerializer
##    ---
##    omit_serializer: true

# EXAMPLE in bash:
#  propid=`curl 'http://127.0.0.1:8000/schedule/getpropid/ct13m/2014-12-25/'`
@api_view(['GET'])
def getpropid(request, tele, date):
    """
    Retrieve a **propid** from the schedule given `telescope` and `date`.
    """
    #! print('DBG-0: getpropid({}, {})'.format(tele, date))
    serializer_class = SlotSerializer
    try:
        slot = Slot.objects.get(obsdate=date, telescope=tele)
        #!propid = slot.propid
        propid = slot.proposals.all()[0]
        return HttpResponse(propid, content_type='text/plain')
    except Exception as err:
        if EmptySlot.objects.filter(obsdate=date, telescope=tele).count() == 0:
            es = EmptySlot(obsdate=date, telescope=tele)
            es.save()
        return HttpResponse('NA', content_type='text/plain')

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
    print('EXECUTING: load_schedule; name={}'.format(uploadedfile.name))
    if uploadedfile.size > maxsize:
        return None
    print("DBG-1: size={}".format(uploadedfile.size))
    xmlstr = ''
    for line in uploadedfile:
        xmlstr += line.decode()
    root = ET.fromstring(xmlstr)
    #!tree = ET.parse(uploadedfile)
    created = root.get('created')
    begin = root.get('begindate')
    end = root.get('enddate')
    print('DBG-2: created={}, begin={}, end={}'.format(created, begin, end))
    print('DBG-3: contains {} entries'.format(len(root)))

    for proposal in root:
        obsdate = datetime.strptime(proposal.get('date'),'%Y-%m-%d').date()
        telescope = proposal.get('telescope')

        propid = proposal.get('propid')
        title=proposal.findtext('title')
        piname=proposal.findtext('piname')
        affiliation=proposal.findtext('affiliation')


        # Never overwrite existing Proposal or Slot
        ddict=dict(pi_name=piname,
                   pi_affiliation=affiliation,
                   title=title)
        prop, pmade = Proposal.objects.get_or_create(pk=propid, defaults=ddict)
        slot, smade = Slot.objects.get_or_create(telescope=telescope,
                                                 obsdate=obsdate)
        if smade:
            slot.proposals.add(prop)
            
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
    #!print('DBG: serializer={}'.format(repr(SlotSerializer())))

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
