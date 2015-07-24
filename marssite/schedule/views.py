from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
import json

# (telescope, date) => propid; date:: YYYY-MM-DD or None=any-date
SCHEDULE = {  
    ('soar',  '2014-12-15'): 'soar',
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

def list(request):
    context = RequestContext(request, {
        'schedule': [(tele,date,prop)
                     for ((tele,date),prop) in SCHEDULE.items()]
    })
    return render(request, 'schedule/list.html', context)


# EXAMPLE in bash:
#  propid=`curl 'http://127.0.0.1:8000/schedule/prop/ct13m/2014-12-25/'`
def schedprop(request, tele, date):
    prop = SCHEDULE.get((tele,date), 'Not-Provided')
    #!data = json.dumps(dict(telescope=tele, date=date, propid=prop))
    #!return HttpResponse(data, content_type='application/json')
    return HttpResponse(prop, content_type='text/plain')
