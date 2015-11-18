from django.shortcuts import render
from django.views.generic import ListView

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics

from .models import Submittal
from .serializers import SubmittalSerializer


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
    
 
