from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Fitsname

# Create your views here.

def index(request):
    fnames = get_list_or_404(Fitsname)
    return render(request,
                  'provisional/index.html',
                  RequestContext(request, {
                      'fitname_list': fnames,
                  }))

def insert(request, dtacqnam, dtnsanam):
    sql='SELECT dtnsanam FROM voi.siap WHERE dtacqnam = %s'
    obs = Image.objects.raw(sql,[dtacqnam])
    return HttpResponse(obs[0], content_type='text/plain')
