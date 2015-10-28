import logging

from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.db import transaction
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework import viewsets
from .models import Fitsname
from .perlport import drop_file
from .serializers import FitsnameSerializer
from siap.queries import get_tada_references

class ProvListView(ListView):
    #model = Fitsname
    limit=2000
    queryset = Fitsname.objects.all().order_by('source')[:limit]

    def get_context_data(self, **kwargs):
        context = super(ProvListView, self).get_context_data(**kwargs)
        context['limit'] = self.limit
        return context
 
@api_view(['GET'])
def index(request, limit=2000):
    delcnt = request.GET.get('delcnt',0)
    fnames = Fitsname.objects.all().order_by('source')[:limit]
    return render(request,
                  'provisional/index.html',
                  RequestContext(request, {
                      'limit': limit,
                      'delcnt': delcnt,
                      'fitname_list': fnames,
                  }))

def stuff_with_tada(request, limit=1000):
    images = get_tada_references(limit=limit)
    for ref,src in images:
        fitsname = Fitsname(id=ref, source=src)
        fitsname.save()
        
    #return redirect(index)
    return redirect('/provisional/')

        
def add(request, reference=None):
    source = request.GET.get('source')
    fitsname = Fitsname(id=reference, source=source)
    fitsname.save()
    return HttpResponse('Added provisional name (id={}, source={})'
                        .format(fitsname.id, fitsname.source), 
                        content_type='text/plain')



@api_view(['GET'])
@transaction.atomic
def rollback(request):
    'Remove all provisionaly added files from DB'
    from . import perlport
    from django.db import connection

    logging.debug('EXECUTING: mars:provisional/rollback()')

    ref_list = [fn.id for fn in Fitsname.objects.all()]
    delcnt = len(ref_list)
    Fitsname.objects.all().delete()
    cursor = connection.cursor()
    for ref in ref_list:
        drop_file(cursor, ref)

    return redirect('/provisional/?delcnt=delcnt') 

@transaction.atomic
def dbdelete(request, reference=None):
    '''Delete a fits file from the archive DB (all tables).'''
    from . import perlport
    from django.db import connection

    cursor = connection.cursor()
    Fitsname.objects.filter(id=reference).delete()
    results = drop_file(cursor, reference)
    #!return HttpResponse(('Number of rows affected for file {} = {}'
    #!                     .format(reference, results)),
    #!                    content_type='text/plain')
    return redirect('/provisional/') 


# ViewSets define the view behavior.
class FitsnameViewSet(viewsets.ModelViewSet):
    queryset = Fitsname.objects.all()
    serializer_class = FitsnameSerializer

