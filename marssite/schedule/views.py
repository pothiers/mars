from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import UploadFileForm
from .models import Slot
from .upload import handle_uploaded_file

import json
import subprocess
from datetime import date, datetime, timedelta as td
import xml.etree.ElementTree as ET



def list(request, limit=4000):
    slots = Slot.objects.all()[:limit]
    return render(request,
                  'schedule/list.html',
                  RequestContext(request, {
                      'limit': limit,
                      'slot_list': slots,
                  })
                  )


# EXAMPLE in bash:
#  propid=`curl 'http://127.0.0.1:8000/schedule/getpropid/ct13m/2014-12-25/'`
def getpropid(request, tele, date):
    propid = Slot.objects.get(obsdate=date,telescope=tele)
    #!data = json.dumps(dict(telescope=tele, date=date, propid=prop))
    #!return HttpResponse(data, content_type='application/json')
    return HttpResponse(propidcontent_type='text/plain')

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


@csrf_protect
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('schedule/upload.html', {'form': form})    
