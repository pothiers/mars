from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Image

# Create your views here.

def index(request):
    im_list = Image.objects.raw('SELECT * FROM voi.siap LIMIT 25') #!!! not all
    template = loader.get_template('siap/index.html')
    context = RequestContext(request, {
        'recent_image_list': im_list,
    })
    #!output = '<br />'.join([im.reference for im in im_list])
    return HttpResponse(template.render(context))

def filenames(request, propid):
    output = '<table border="1"> '
    for im in Image.objects.raw("SELECT * FROM voi.siap WHERE prop_id = '{}' LIMIT 25".format(propid)): #!!! limit 
        output += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(im.dtpropid, im.dtnsanam, im.dtacqnam)
    return HttpResponse("Files for prop_id: %s<p>%s" % (propid,output))

def detail(request, image_id):
    im_list = Image.objects.raw("SELECT * FROM voi.siap WHERE reference = '{}'".format(image_id))
    template = loader.get_template('siap/detail.html')
    context = RequestContext(request, {
        'dict': im_list[0].__dict__,
    })

    #return HttpResponse("Details for image: %s<p>%s" % (image_id,im_list[0].__dict__))
    return HttpResponse(template.render(context))
