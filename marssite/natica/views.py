from django.shortcuts import render
from django.http import JsonResponse
from os import listdir, path
from os.path import isfile, join, abspath
import json


# Stub for future work to generate links from NFS mount for downloads
def _generateFileLinks(results):
    pass

# create the lookup paths for the various js resources
def _getResources(appname):
    # get the resource names for html
    curdir = path.dirname(__file__)
    resPath = path.join(curdir,"../static/natica/dist")
    stats = open(path.join(curdir, "webpack-assets.json"), 'r')
    resources = json.loads(stats.read())
    r = []

    # manifest & app are removed and added in proper order here because order matters at load time
    r.append(resources.pop('manifest')['js'])
    app = resources.pop(appname)
    for js in resources:
        if js.find("bundle") > -1:
            # skip the unwanted app code
            continue
        r.append(resources[js]['js'])
    r.append(app['js'])
    return r



def search(request):
    r = _getResources("app.bundle")
    return render(request, "search.html", {"jsResources":r })


def staging(request):
    r = _getResources("staging.bundle")
    print(r)
    return render(request, "staging.html", {'jsResources':r})

