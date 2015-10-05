from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic.list import ListView

def home(request):
    context = RequestContext(request, {
    })
    return render(request, 'water/home.html', context)
