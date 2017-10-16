from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from os import listdir, path, mkdir
from django.conf import settings
from os import mkdir, chdir,symlink
from os.path import isfile, join, abspath
import json
import requests
from siap import queries
"""
Assume there are some mount points on this machine
one will have the archive files
another will have the ftp directories

This needs to get a list of files (selected by the user) and create
relative symlinks from the archive to the ftp directory owned by the user
"""

ftpdirs = "/srv/ftp"
ftppasswd = "/srv/ftp/ftp-passwd/pureftpd.passwd"
dev = True

def _linkfile(fname, uname):
    userdir = join(ftpdirs, 'anon', uname)
    if path.isdir(userdir) == False:
        mkdir(userdir)
    chdir(userdir)
    # make the file too for testing
    if dev:
        filepath = queries.get_fits_location(fname)

        # create directories if not already made
        dirs = path.basename(fname).split("/") 
        dirs = dirs[1:]
        nfspath = join(ftpdirs,"nfsmount")
        
        for dr in dirs:
            nfspath = join(nfspath,dr)
            if path.isdir(nfspath) == False:
                mkdir(nfspath)

                
        f= open(join(ftpdirs, "nfsmount", filename), 'w')
        f.write("the filename is {}".format(queries.get_fits_location(fname))) 

        # adjust the actual file pathname location to match mounted location
        f.close()
    try:
        symlink("../../nfsmount/{}".format(fname), "./{}".format(fname))
    except:
        pass # symlink already exists?

@csrf_exempt
def stagefiles(request):
    message = ""
    if len(request.body) > 0:
        body = request.body.decode('utf-8')
        data = json.loads(body)
        for record in data["files"]:
            _linkfile(record['file']['reference'], "user_123")
    else:
        return JsonResponse({'message':'Error, no data provided', 'status':'error'})
     
    # ftp directories mounted at /srv/ftp
    
    # check if user loggedin, put links in user dir - get from ldap

    # otherwise generate a guest user directory in the anonymous ftp
    # directory
    return JsonResponse({'message':'ok', 'status':'ok'})

def downloadsinglefile(request):
    filename = request.GET.get('f', '')
    filepath = join(ftpdirs, 'nfsmount' )
    if dev:
        filepath = join(filepath, filename)
    else:
        filepath = join(filepath, queries.get_fits_location(fileame))
    response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filepath)
    response['X-Accel-Redirect'] = smart_str(filepath)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response

# create the lookup paths for the various js resources
def _getResources(appname):
    # get the resource names for html
    curdir = path.dirname(__file__)
    resPath = path.join(curdir,"../static/portal/dist")
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
    return render(request, "staging.html", {'jsResources':r})
