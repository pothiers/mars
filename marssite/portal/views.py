from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.conf import settings
import datetime
import hashlib
import os
from os import path
from shutil import copyfile
import json
import requests
from siap import queries
"""
Assume there are some mount points on this machine
one will have the archive files
another will have the ftp directories

This needs to get a list of files (selected by the user) and create
relative os.symlinks from the archive to the ftp directory owned by the user
"""

ftpdirs = "/srv/ftp"
nfsmount = "/srv/ftp/nfsmount"
ftppasswd = "/srv/ftp/ftp-passwd/pureftpd.passwd"
dev = True if os.environ['ENVIRONMENT'] == "dev" else False

def _linkfile(fname, uname):
    print("Current env is {}".format(dev))
    userdir = os.path.join(ftpdirs, 'anon', uname)
    if os.path.isdir(userdir) == False:
        os.mkdir(userdir)
    nfspath = queries.get_fits_location(fname)
    filepath = os.path.join(ftpdirs,'nfsmount')
    filepath +=  nfspath
    print("##### filepath {}".format(filepath))
    # make the file too for testing
    if dev:
        # create directories if not already made
        dirs = os.path.dirname(nfspath).split("/")
        dirs = dirs[1:]
        storagepath = os.path.join(ftpdirs,"nfsmount")
        for dr in dirs:
            storagepath = os.path.join(storagepath,dr)
            if os.path.isdir(storagepath) == False:
                os.mkdir(storagepath)

        print("Final storagepath is {}".format(storagepath))
        print("About to write to {}".format(filepath))
        f= open(filepath, 'w')
        f.write("the filename is {}".format(nfspath))

        # adjust the actual file pathname location to match mounted location
        f.close()
    try:
        os.symlink("../../nfsmount{}".format(nfspath), "{}/{}".format(userdir,fname))
    except:
        # error is always present, not sure why...
        pass
    return JsonResponse({'message':'done', 'status':'ok'})

@csrf_exempt
def downloadselected(request):
    message = ""
    if len(request.body) > 0:
        body = request.body.decode('utf-8')
        data = json.loads(body)
        # create a zip for download
        # limit to 10 files

        # make a temporary directory
        t = datetime.datetime.now()
        hash = hashlib.md5(str(t).encode("utf-8")).hexdigest()
        tmpdir = "/tmp/{}".format(hash)
        os.mkdir(tmpdir)
        for f in data['files']:
            fpath = nfsmount+queries.get_fits_location(f['file']['reference'])
            copyfile(fpath, os.path.join(tmpdir, f['file']['reference']))
    else:
        return JsonResponse({'message':'Error, no data provided', 'status':'error'})

    # ftp directories mounted at /srv/ftp

    # check if user loggedin, put links in user dir - get from ldap

    # otherwise generate a guest user directory in the anonymous ftp
    # directory
    return JsonResponse({'message':'ok', 'status':'ok'})

def downloadsinglefile(request):
    filename = request.GET.get('f', '')
    filepath = os.path.join(ftpdirs, 'nfsmount' )
    filepath += queries.get_fits_location(filename)
    response = HttpResponse(filepath,content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['X-Accel-Redirect'] = smart_str(filepath)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response

# create the lookup paths for the various js resources
def _getResources(appname):
    # get the resource names for html
    curdir = os.path.dirname(__file__)
    resPath = os.path.join(curdir,"../static/portal/dist")
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

"""
  Staging will setup either all the resultset or as selected subset based on a get variable
  @get(stage) ["all", "selected"]
  @post(selectedFiles) - When staging subset
"""
@csrf_exempt
def staging(request):
    message = ""
    """
    Are we staging a subset or the entire result set?
    """
    stageAll = True if request.GET.get("stage", "") == "all" else False

    if stageAll:
        # get the query used to generate the last result set
        # save the query in the user's session to pull it back out
        # iterate through the results to generate links
        pass
    else:
        fileList = request.POST.get("selectedFiles")
        if len(fileList) > 0:
            data = json.loads(fileList)
            for record in data:
                _linkfile(record['reference'], "user_123")
        else:
            response = render_to_response('500.html', {"message":"No files were selected"},
                                    context_instance=RequestContext(request))
            response.status_code = 500
            return response


    r = _getResources("staging.bundle")

    return render(request, "staging.html", {'jsResources':r})
