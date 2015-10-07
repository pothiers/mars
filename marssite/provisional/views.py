from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import RequestContext
from .models import Fitsname

# Create your views here.

def index(request):
    fnames = get_list_or_404(Fitsname.objects.all())
    return render(request,
                  'provisional/index.html',
                  RequestContext(request, {
                      'fitname_list': fnames,
                  }))


def add(request, reference=None):
    source = request.GET.get('source')
    fitsname = Fitsname(id=reference, source=source)
    fitsname.save()
    return HttpResponse('Added provisional name (id={}, source={})'
                        .format(fitsname.id, fitsname.source), 
                        content_type='text/plain')
