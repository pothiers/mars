from django.shortcuts import render
from django.http import HttpResponse
from .models import Image

# Create your views here.

def index(request):
    im_list = Image.objects.raw('SELECT * FROM voi.siap LIMIT 5') #!!! limit 5
    output = '<br />'.join([im.reference for im in im_list])
    return HttpResponse(output)

def filenames(request, propid):
    output = '<table border="1"> '
    for im in Image.objects.raw("SELECT * FROM voi.siap WHERE prop_id = '{}' LIMIT 5".format(propid)): #!!! limit 5
        output += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(im.dtpropid, im.dtnsanam, im.dtacqnam)
    return HttpResponse("Details for image: %s<p>%s" % (propid,output))
                        

