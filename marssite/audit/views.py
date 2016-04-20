from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.decorators import  api_view,parser_classes

from .models import Submittal, SourceFile
from .serializers import SubmittalSerializer


# curl http://localhost:8000/audit/ > ~/Downloads/list.json
class SubmittalList(generics.ListAPIView):
    model = Submittal
    queryset = Submittal.objects.all()
    template_name = 'audit/submittal_list.html'

    serializer_class = SubmittalSerializer
    paginate_by = 50

class SubmittalDetail(generics.CreateAPIView):
    model = Submittal
    queryset = Submittal.objects.all()
    template_name = 'audit/submittal_detail.html'
    serializer_class = SubmittalSerializer


    #curl -H "Content-Type: application/json" -X POST -d '{"source":"xyz","archive":"xyz","status":"NA1", "metadata":"NA2"}' http://localhost:8000/audit/add
@csrf_exempt
@api_view(['POST'])
@parser_classes((JSONParser,))
def add_submit(request):
    """Add a SUBMIT record using JSON data."""
    #print('DBG: audit/add_submit. Request={}'.format(request))
    if request.method == 'POST':
        #!print('Raw Data: "{}"'.format(request.body))
        #!print('Parsed Data: "{}"'.format(request.data))
        #!print('source={}'.format(request.data['source']))
        obj = Submittal(**request.data)
        obj.save()
    return redirect(reverse('audit:submittal_list'))

@csrf_exempt
def submitted(request):
    """Record list of source paths as submitted for ingest.
EXAMPLE:    
    curl -X POST -d '/04202016/tele/img1.fits /04202016/tele/img2.fits' http://localhost:8000/audit/submitted/
    """


    if request.method == 'POST':
        paths = request.body.decode('utf-8').strip().split()
        SourceFile.objects.bulk_create([SourceFile(source=path) for path in paths])
    return redirect(reverse('audit:submittal_list'))
