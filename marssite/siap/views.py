from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Image
from django.views.generic.list import ListView

def index(request):
    sql='SELECT * FROM voi.siap LIMIT 25' #!!! not all
    context = RequestContext(request, {
        'recent_image_list': Image.objects.raw(sql) 
    })
    return render(request, 'siap/index.html', context)

def getnsa(request, dtacqnam):
    sql='SELECT dtnsanam FROM voi.siap WHERE dtacqnam = %s'
    obs = Image.objects.raw(sql,[dtacqnam])
    return HttpResponse(obs[0], content_type='text/plain')

def getacq(request, dtnsanam):
    sql='SELECT dtacqnam FROM voi.siap WHERE dtnsanam = %s'
    obs = Image.objects.raw(sql,[dtnsanam])
    return HttpResponse(obs[0], content_type='text/plain')

def filenames(request, propid):
    context = RequestContext(request, {
        'propid': propid,
        'image_list': Image.objects.raw("SELECT * FROM voi.siap  WHERE prop_id = %s",[propid])
    })
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
    context = RequestContext(request, {
        #!'dict': im.__dict__,
        'dict': im_list[0].__dict__,
    })
    return render(request, 'siap/detail.html', context)