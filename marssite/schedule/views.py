from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import SlotSetForm
from .models import Slot, EmptySlot
from .upload import handle_uploaded_file
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route, api_view
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
#@csrf_exempt
def upload_file(request):
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



@api_view(['GET'])
def list(request, limit=100):
    #slots = Slot.objects.all()
    slots = Slot.objects.all()[:limit]
    return render(request,
                  'schedule/list.html',
                  RequestContext(request, {
                      'title': 'All',
                      'limit': limit,
                      'slot_list': slots,
                  })
                  )
@api_view(['GET'])
@list_route(methods=['get'])
def list_empty(request, limit=4000):
    slots = EmptySlot.objects.all()[:limit]
    return render(request,
                  'schedule/list_empty.html',
                  RequestContext(request, {
                      'limit': limit,
                      'slot_list': slots,
                  })
                  )

def list_day(request, date, limit=1000):
    slots = Slot.objects.filter(obsdate=date)[:limit]
    return render(request,
                  'schedule/list.html',
                  RequestContext(request, {
                      'title': 'Day: {}'.format(date),
                      'limit': limit,
                      'slot_list': slots,
                  })
                  )


##    request_serializer: ScheduleQuerySerializer
##    response_serializer: ScheduleSerializer

# EXAMPLE in bash:
#  propid=`curl 'http://127.0.0.1:8000/schedule/getpropid/ct13m/2014-12-25/'`
@api_view(['GET'])
def getpropid(request, tele, date):
    '''
    Retrieve a **propid** from the schedule given `telescope` and `date`.
    ---
    omit_serializer: true
    '''
    try:
        slot = Slot.objects.get(obsdate=date,telescope=tele)
        propid = slot.propid
        return HttpResponse(propid, content_type='text/plain')
    except Exception as err:
        if EmptySlot.objects.filter(obsdate=date,telescope=tele).count() == 0:
            es = EmptySlot(obsdate=date,telescope=tele)
            es.save()
        return HttpResponse('', content_type='text/plain')
                

# OBSOLETE!
def scrape(request,begindate, enddate):
    telescope_list = ('ct09m,ct13m,ct15m,ct1m,ct4m,gem_n,gem_s,het,'
                      'keckI,keckII,kp09m,kp13m,kp21m,kp4m,kpcf,'
                      'magI,magII,mmt,soar,wiyn').split(',')

    cmdstr = ('/home/pothiers/sandbox/mars/marssite/schedule/getschedulexml.pl '
              '-tel={telescope} -date={date}')
    bdate = datetime.strptime(begindate,'%Y-%m-%d').date()
    edate = datetime.strptime(enddate,'%Y-%m-%d').date()
    delta = edate - bdate
    ns = dict(noao="http://www.noao.edu/proposal/noao/", )

    for i in range(delta.days + 1):
        obsdate = bdate + td(days=i)
        for tele in telescope_list:
            out = subprocess.check_output(cmdstr.format(telescope=tele,
                                                        date=obsdate),
                                          shell=True)
            #!print(out, file=f)
            if len(out) < 3:
                continue
            root = ET.fromstring(out)
            prop_el = root.find('.//proposal')
            if prop_el == None:
                continue
            tele_el = root.find('.//parameter[@name="telescope"]')
            date_el = root.find('.//parameter[@name="date"]')

            yyyymmdd = datetime.strptime(date_el.text,'%Y-%m-%d').date()
            slot = Slot(telescope = tele_el.text,
                        obsdate = yyyymmdd,
                        propid = prop_el.get('{{{noao}}}id'.format(**ns)) )
            slot.save()

    return HttpResponse('Scraped schedule info for dates {} to {}.'
                        .format(begindate, enddate),
                        content_type='text/plain')


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

    for proposal in root:
        obsdate = datetime.strptime(proposal.get('date'),'%Y-%m-%d').date()
        telescope = proposal.get('telescope')
        propid = proposal.get('propid')
        title=proposal.findtext('title')
        piname=proposal.findtext('piname')
        affiliation=proposal.findtext('affiliation')
        #! print('DBG-3: telescope={}, obsdate={}, propid={}'.format(telescope, obsdate, propid))
        #! print('DBG-3.2: title={}, pi={}, affil={}'.format(title, pi, affil))
        
        Slot.objects.filter(telescope=telescope, obsdate=obsdate).delete()
        slot = Slot(telescope = telescope, obsdate = obsdate, propid = propid,
                    pi_name=piname,
                    pi_affiliation=affiliation,
                    title=title
        )
        slot.save()
    return redirect('/schedule/')



class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()[:99]
    serializer_class = SlotSerializer
