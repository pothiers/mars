'''
Proof of concept download service: 
1. by archive filename, only for publice release fits
2. by params on URL: 
   obsdate
   ra
   dec
   original filename
   substring of archive filename
   telescope
   instrument
   propid
   (others)
'''
import json
import re

from django.db import connection
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.generic.list import ListView
from django.template.context_processors import csrf
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import detail_route, list_route, api_view

from .tables import SiapTable
from .models import Image, VoiSiap
from .forms import VoiSiapForm
from .queries import get_tada_references, get_like_archfile, get_from_siap



def index(request):
    'SIAP index of subset of all files.'
    limit=250
    sql = 'SELECT count(*) FROM voi.siap;'
    sql2='SELECT * FROM voi.siap LIMIT {}'.format(limit) #!!! not all
    from django.db import connection
    #!cursor = connection.cursor()
    #!cursor.execute( sql )
    #!total = cursor.fetchone()[0]
    context = {
        #!'total_image_count': total,
        'limit_count': limit,
        'recent_image_list': Image.objects.raw(sql2) ,
    }

    return render(request, 'siap/index.html', context)

# Regex search takes almost 20 seconds to search 11.3 million records
def tada(request): 
    'List of SIAP files containing TADA in Archive filename.'
    limit = 2000
    images = get_tada_references(limit=limit)
    #! images = [r[0] for r in cursor.fetchall()]
    #!for im in images:
    #!    print('Image={}'.format(im))
    print('request.content_type={}'.format(request.META.get('CONTENT_TYPE')))
    
    context = {
        'limit_count': limit,
        'tada_images': images, # Image.objects.raw(sql),
    }

    if request.META.get('CONTENT_TYPE','none') == 'application/json':
        return JsonResponse([im[0] for im in images], safe=False)
    if request.META.get('CONTENT_TYPE','none') == 'text/csv':
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tada.csv"'
        writer = csv.writer(response)
        for im in images:
            writer.writerow(im)
        return response
    else:
        return render(request, 'siap/tada.html', context)
    
def getnsa(request, dtacqnam):
    sql='SELECT dtnsanam FROM voi.siap WHERE dtacqnam = %s'
    obs = Image.objects.raw(sql,[dtacqnam])
    return HttpResponse(obs[0], content_type='text/plain')

def getacq(request, dtnsanam):
    sql='SELECT dtacqnam FROM voi.siap WHERE dtnsanam = %s'
    obs = Image.objects.raw(sql,[dtnsanam])
    return HttpResponse(obs[0], content_type='text/plain')

def filenames(request, propid):
    context = {
        'propid': propid,
        'image_list': Image.objects.raw("SELECT * FROM voi.siap  WHERE prop_id = %s",[propid])
    }
    return render(request, 'siap/filenames.html', context)

class FileListView(ListView):
    model = Image

    def get_context_data(self, **kwargs):
        context = super(FileListView, self).get_context_data(**kwargs)
        context['image_list'] = Image.objects.raw("SELECT * FROM voi.siap  WHERE prop_id = %s",[propid])
        return context    

def detail(request, image_id):
    #!im = get_object_or_404(Image, pk=image_id)
    im_list = (Image.objects
               .raw("SELECT * FROM voi.siap WHERE reference = %s", [image_id]))
    context = {'dict': im_list[0].__dict__ }
    return render(request, 'siap/detail.html', context)

# NB: raw SQL is string with FORMATTING PARAMETERS so '%' indicates paramter.
#     Double any occurances to protect from interpretation.
# curl -H "Content-Type: application/json" -X POST -d '{"sql":"xyz","bitcoins":"100"}' http://localhost:8000/siap/arch/query
#
# cat <<EOF > foo.json
# {"sql":"SELECT * FROM voi.siap WHERE reference LIKE '%%TADA%%' ", "bitcoins":"100"}
# EOF
# curl -H "Content-Type: application/json" -X POST -d @foo.json http://localhost:8000/siap/arch/query
#@api_view(['POST'])
@csrf_exempt
def query_by_json(request, format='json', cols=None, where=None, limit=None):
    'Upload a file constaining SQL that does a SELECT against SIAP table.'
    print('EXECUTING: views<siap>:query_by_file; method={}'
          .format(request.method))
    # Easy way to test post???
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        print('body={}'.format(body))
        jsql = body['sql']
        cursor = connection.cursor()
        # Force material view refresh
        cursor.execute('SELECT * FROM refresh_voi_material_views()') 
        #!cursor.fetchall()
        #!cursor.execute( jsql )
        #!total = cursor.rowcount
        #!results = cursor.fetchall()
        #print('results={}'.format(results))
        qs = VoiSiap.objects.raw(jsql)
        print('qs={}'.format(list(qs)))
        print('serialized results={}'.format(serializers.serialize(format, qs)))
        return JsonResponse(serializers.serialize(format, qs), safe=False)
    elif request.method == 'GET':
        print('get qdict lists={}'.format(list(request.GET.lists())))
        format = request.GET.get('format', 'json')
        cols = request.GET.get('cols', '*')
        where = request.GET.get('where', None)
        limit  = request.GET.get('limit', '2')
        sql = ('SELECT {} FROM voi.siap {} {}'
               .format(cols,
                       'WHERE '+where if where != None else '',
                       'LIMIT '+limit if limit != None else ''))
        #return HttpResponse('No SQL given so there are no results!')
        #!print('raw sql={}'.format(sql))
        #!qs = VoiSiap.objects.raw(sql)
        #!print('qs={}'.format(list(qs)))
        #!print('serialized results={}'.format(serializers.serialize('json',qs)))
        cursor = connection.cursor()
        # Force material view refresh
        cursor.execute('SELECT * FROM refresh_voi_material_views()') 
        cursor.fetchall()
        cursor.execute( sql )
        total = cursor.rowcount
        results = cursor.fetchall()
        return HttpResponse(results)

siapsqlre = re.compile(r"(?i)SELECT\s+\S+\s+FROM\s+voi.siap\s+"    )
def validate_sql(sql):
    "Require SQL like:  SELECT <fields> FROM voi.siap <something>"
    if siapsqlre.match(sql):
        return True, None
    else:
        return False, ('SQL must be of format: '
                       '"SELECT <field>[,<field>...] '
                       'FROM voi.siap <something>"; Got: {}\n'.format(sql))

    # curl "Content-Type: application/json" -X POST --data-binary @sql/tada-files.sql http://localhost:8000/siap/squery 
@csrf_exempt
def query_by_sql(request, format='json', refresh_view=True):
    'POST  payload is SQL string that does a SELECT against SIAP table.'
    # To test post:
    # curl -X POST --data-binary @sql/tada-files.sql http://localhost:8000/siap/squery
    # Text mode MIGHT work (depending on whitepace particulars):
    # curl -X POST -d @sql/tada-files.sql http://localhost:8000/siap/squery 
    # curl -X POST -d 'SELECT reference FROM voi.siap LIMIT 2' http://localhost:8000/siap/squery
    print('DBG-0: siap/views.py:query_by_sql()')
    if request.method == 'POST':
        sql = ' '.join(request.body.decode('utf-8').strip().split())
        print('DBG-1: siap/views.py:query_by_sql(); sql="{}"'.format(sql))
        validsql, message = validate_sql(sql)
        if validsql:
            cursor = connection.cursor()
            # Force material view refresh
            #! cursor.execute('SELECT * FROM refresh_voi_material_views()') 
            #! cursor.fetchall()

            cursor.execute( sql )
            total = cursor.rowcount
            results = cursor.fetchall()
            print('results={}'.format(results))
            return HttpResponse('\n'.join(['\t'.join([str(v) for v in tup])
                                           for tup in results])+'\n')
        else:
            return HttpResponse('ERROR: '+message)
@csrf_exempt
def query_by_str(request, format='json'):
    'POST  payload is string of SQL that does a SELECT against SIAP table.'
    # To test post:
    # curl -H "Content-Type: application/json" -X POST --data-binary @sql/tada-files.sql http://localhost:8000/siap/arch/query 
    print('DBG-0: siap/views.py:query_by_str()')
    if request.method == 'POST':
        sql = ' '.join(request.body.decode('utf-8').strip().split())
        print('DBG-1: siap/views.py:query_by_str(); sql={}'.format(sql))
        cursor = connection.cursor()
        # Force material view refresh
        cursor.execute('SELECT * FROM refresh_voi_material_views()') 
        #!cursor.fetchall()
        #!cursor.execute( sql )
        #!total = cursor.rowcount
        #!results = cursor.fetchall()
        #print('results={}'.format(results))
        qs = VoiSiap.objects.raw(sql)
        print('qs={}'.format(list(qs)))
        print('serialized results={}'.format(serializers.serialize(format, qs)))
        return JsonResponse(serializers.serialize(format, qs), safe=False)
        
    #!c = {'form': form}
    #!c.update(csrf(request))
    #!resdict = dict(sql=sql, results=list(results))
    #!print('resdict={}'.format(resdict))

def query(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VoiSiapForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VoiSiapForm()

    return render(request, 'siap/siap.html', {'form': form})        

@api_view(['GET'])
def lame_query_by_url(request):
    """Simple query using URL paramaters."""
    limit = int(request.GET.get('limit','100'))
    archfile = request.GET.get('archfile')
    images = get_like_archfile(archfile, limit=limit)

    context = {
        'limit_count': limit,
        'tada_images': images, # Image.objects.raw(sql),
    }

    if request.META.get('CONTENT_TYPE','none') == 'application/json':
        return JsonResponse([im[0] for im in images], safe=False)
    if request.META.get('CONTENT_TYPE','none') == 'text/csv':
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tada.csv"'
        writer = csv.writer(response)
        for im in images:
            writer.writerow(im)
        return response
    else:
        return render(request, 'siap/tada.html', context)



# http://localhost:8000/siap/query/?date_obs=02-28-2006&reference=k21i
# curl -H "Content-Type: text/csv" http://localhost:8000/siap/query/?limit=10
@api_view(['GET'])
def query_by_url(request):
    """
    Simple query using URL paramaters.
    **Context**
    ``query_results_table``
        Table of useful SIAP columns as list of dictionaries. 
    
    **Template:**

    :tempalate:`siap/siap-subset.html`
    """
    getdict = dict(request.GET.items())
    sortval = getdict.pop('sort',None)
    rows = get_from_siap(**getdict)
    #print('rows={}'.format(rows))

    table = SiapTable(rows)
    context = {
        'query_results_table': table,
        'limit_count': 99, #!!!
        'title': 'Results of SIAP query via MARS URL parameters',
    }

    if request.META.get('CONTENT_TYPE','none') == 'application/json':
        return JsonResponse([row['reference'] for row in rows], safe=False)
    if request.META.get('CONTENT_TYPE','none') == 'text/csv':
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="siap.csv"'
        
        writer = csv.DictWriter(response, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return response
    else:
        return render(request, 'siap/siap-subset.html', context)
    
