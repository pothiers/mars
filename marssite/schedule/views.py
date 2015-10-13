from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Slot
import json
import subprocess
from datetime import date, datetime, timedelta as td
import xml.etree.ElementTree as ET


# (telescope, date) => propid; date:: YYYY-MM-DD or None=any-date
SCHEDULE = {
    # DTTELESC DTCALDAT       DTPROPID
    ('soar',  '2014-12-15'): 'soar',
    ('soar',  '2014-12-19'): 'soar',
    ('ct4m',   None       ): 'test-prop',    
    ('ct13m', '2014-12-25'): 'smarts',
    ('ct15m',  None       ): 'test-prop',  
    ('ct1m',   None       ): 'test-prop',   
    ('ct09m',  None       ): 'test-prop',   
    ('ctlab',  None       ): 'test-prop',  
    ('kp4m',   None       ): 'test-prop',  
    ('kp35m',  None       ): 'test-prop',  
    ('kp21m',  None       ): 'test-prop',  
    ('kpcf',   None       ): 'test-prop',  
    ('kp09m',  None       ): 'test-prop',  
    ('bok23m', None       ): 'test-prop',
}

def list(request, limit=2000):
    slots = Slot.objects.all()[:limit]
    return render(request,
                  'schedule/list.html',
                  RequestContext(request, {
                      'limit': limit,
                      'slot_list': slots,
                  })
                  )


# EXAMPLE in bash:
#  propid=`curl 'http://127.0.0.1:8000/schedule/prop/ct13m/2014-12-25/'`
def schedprop(request, tele, date):
    prop = SCHEDULE.get((tele,date), 'Not-Provided')
    #!data = json.dumps(dict(telescope=tele, date=date, propid=prop))
    #!return HttpResponse(data, content_type='application/json')
    return HttpResponse(prop, content_type='text/plain')

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
