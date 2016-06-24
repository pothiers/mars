from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

def home(request):
    version = 'version 2016.06.23b'
    context = {
        'mars_version': version,
        'dbhost': settings.DATABASES['default']['HOST'],
    }
    return render(request, 'water/home.html', context)

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'today': reverse('schedule:today_list',
                         request=request, format=format),
        'upload': reverse('schedule:upload_file',
                          request=request, format=format),
        'empty': reverse('schedule:list_empty',
                         request=request, format=format)
    })
