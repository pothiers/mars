from django.shortcuts import render
from django.http import JsonResponse
from os import listdir, path
from os.path import isfile, join, abspath
import json

# Create your views here.


def search(request):
    # get the resource names for html
    curdir = path.dirname(__file__)
    resPath = path.join(curdir,"../static/natica/dist")
    
    stats = open(path.join(curdir, "webpack-assets.json"), 'r')
    resources = json.loads(stats.read())
    r = []
    r.append(resources.pop('manifest')['js'])
    app = resources.pop('app.bundle')
    for js in resources:
        r.append(resources[js]['js'])
    r.append(app['js'])

    return render(request, "search.html", {"jsResources":r })


