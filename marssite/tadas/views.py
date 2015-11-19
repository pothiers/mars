from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.decorators import  api_view,parser_classes

from .models import Submittal
from .serializers import SubmittalSerializer


# curl http://localhost:8000/tadas/ > ~/Downloads/list.json
class SubmittalList(generics.ListAPIView):
    model = Submittal
    queryset = Submittal.objects.all()
    template_name = 'tadas/submittal_list.html'

    serializer_class = SubmittalSerializer
    paginate_by = 50

class SubmittalDetail(generics.CreateAPIView):
    model = Submittal
    queryset = Submittal.objects.all()
    template_name = 'tadas/submittal_detail.html'
    serializer_class = SubmittalSerializer

    
# curl -H "Content-Type: application/json" -X POST -d '{"source":"xyz","archive":"xyz","status":"NA", "metadata":"NA"}' http://localhost:8000/tadas/add/ 
@csrf_exempt
@api_view(['POST'])
@parser_classes((JSONParser,))
def add_submit(request):
    """Add a SUBMIT record using JSON data."""
    #if request.is_ajax():
    if request.method == 'POST':
        print('Raw Data: "{}"'.format(request.body   ))
        print('Parsed Data: "{}"'.format(request.data   ))
        print('source={}'.format(request.data['source']))
        obj = Submittal(**request.data)
        print('obj={}'.format(obj))
        obj.save()
    return HttpResponse('Under Construction', content_type='text/plain')    
