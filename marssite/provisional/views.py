import logging

from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.conf import settings

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
    'List all files provisionaly added to DB'
    delcnt = request.GET.get('delcnt',0)
    #fnames = Fitsname.objects.all().order_by('source')[:limit]
    fnames = Fitsname.objects.all()
    return render(request,
                  'provisional/index.html',
                  {
                      #'limit': limit,
                      'delcnt': delcnt,
                      'dbhost': settings.DATABASES['default']['HOST'],
                      'fitname_list': fnames,
                  })

def stuff_with_tada(request, limit=1000):
    print('Stuff with TADA')
    images = get_tada_references(limit=limit)
    print('...got {} images'.format(len(images)))
    for ref,src in images:
        fitsname = Fitsname(id=ref, source=src)
        print('...ref={}, src={}'.format(ref,src))
        fitsname.save()
        
    #return redirect(index)
    print('all stuffed')
    return redirect('/provisional/')

        
def add(request, reference):
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

    # Force material view refresh
    cursor.execute('SELECT * FROM refresh_voi_material_views()')
    cursor.fetchall()
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

