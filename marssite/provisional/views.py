from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.db import transaction
from .models import Fitsname
from .perlport import drop_file

# Create your views here.

def index(request):
    fnames = get_list_or_404(Fitsname.objects.all())
    return render(request,
                  'provisional/index.html',
                  RequestContext(request, {
                      'fitname_list': fnames,
                  }))

    
def add(request, reference=None):

    cursor = connection.cursor()
    sql0 = ("SELECT fits_data_product_id FROM viewspace.fits_data_product "
            "WHERE reference='{}';".format(reference))
    cursor.execute(sql0)
    file_id = cursor.fetchone()[0]

    fitsname = Fitsname(id=reference, source=request.GET.get('source'))

    fitsname.save()
    return HttpResponse('Added provisional name (id={}, source={})'
                        .format(fitsname.id, fitsname.source), 
                        content_type='text/plain')




@transaction.atomic
def dbdelete(request, reference=None):
    '''SCAFFOLDING: Only COUNT (instead of delete) records!!!
 Delete a fits file from the archive DB (all tables).'''
    from . import perlport
    from django.db import connection

    cursor = connection.cursor()

    #!results = drop_file(cursor, reference)
    #!return HttpResponse(('Counts for {}: \n'+'\n'.join(results))
    #!                    .format(reference),
    #!                    content_type='text/plain')

    results = drop_file(cursor, reference)
    return HttpResponse(('Number of rows affected for file {} = {}'
                         .format(reference, results)),
                        content_type='text/plain')
 
