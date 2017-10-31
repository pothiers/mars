from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.conf import settings
from shutil import copyfile
from os import path
from siap import queries
import datetime
import tempfile
import dal
import time
import hashlib
import zipfile
import os
import json
import requests
import logging
"""
Assume there are some mount points on this machine
one will have the archive files
another will have the ftp directories

This needs to get a list of files (selected by the user) and create
relative os.symlinks from the archive to the ftp directory owned by the user
"""

logger = logging.getLogger(__name__)
ftpdirs = "/srv/ftp"
nfsmount = "" # used to map the nfs dir, but this should be mounted at the default location
ftppasswd = "/srv/ftp/ftp-passwd/pureftpd.passwd"
dev = True if os.environ['ENVIRONMENT'] == "dev" else False

missingFiles = []


def _linkfile(fname, uname):
    userdir = os.path.join(ftpdirs, 'anon', uname)
    if os.path.isdir(userdir) == False:
        os.mkdir(userdir)
    nfspath = queries.get_fits_location(fname)
    filepath = os.path.join(ftpdirs,'nfsmount')
    filepath +=  nfspath

    # make the file for testing
    if dev:
        # create directories if not already made
        dirs = os.path.dirname(nfspath).split("/")
        dirs = dirs[1:]
        storagepath = os.path.join(ftpdirs,"nfsmount")
        for dr in dirs:
            storagepath = os.path.join(storagepath,dr)
            if os.path.isdir(storagepath) == False:
                os.mkdir(storagepath)

        f= open(filepath, 'w')
        f.write("the filename is {}".format(nfspath))

        # adjust the actual file pathname location to match mounted location
        f.close()
    try:
        if False == os.path.isfile("/srv/ftp/nfsmount{}".format(nfspath)):
            missingFiles.append(fname)
            return False
        os.symlink("../../nfsmount{}".format(nfspath), "{}/{}".format(userdir,fname))
    except:
        # error is always present, not sure why...
        pass
    return fname

def dirSorter(elem):
    dir = elem.split("_")
    if len(dir) < 2:
        return 0
    if dir[1].isdigit() == False:
        return 0
    return int(dir[1])

def getUserName(request):
    if request.session.get('username', False):
        return request.session['username']
    dirs = os.listdir("/srv/ftp/anon")
    if len(dirs) == 0:
        nextdir = 0
    else:
        topdir = sorted(dirs, key=dirSorter, reverse=True)[0]
        nextdir = int(topdir.split("_")[1])

    name = "user_{}".format(nextdir + 1)
    logger.info("STAGING:NEWUSERCREATED:{}".format(name))
    request.session['username'] = name
    return name

@csrf_exempt
def downloadselected(request):
    message = ""
    if len(request.body) > 0:
        data = json.loads(request.POST.get("selected","[]"))
        # create a zip for download
        # limit to 10 files
        logger.info("STAGING:DOWNLOAD:{} Files requested:{}".format(len(data), getUserName(request)))
        tmp = tempfile.TemporaryFile()
        zf = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
        for f in data[:10]:
            fpath = nfsmount+queries.get_fits_location(f['file']['reference'])
            zf.write(os.path.abspath(fpath), f['file']['reference'])

        zf.close()

        size = tmp.tell()
        tmp.seek(0)
        response = HttpResponse(tmp, content_type="application/zip")
        response['Content-Disposition'] = "attachement; filename={}".format(getUserName(request)+".zip")
        response['Content-Length'] = size

        response['X-Accel-Redirect'] = getUserName(request)+".zip"
        return response

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
    response['X-Accel-Redirect'] = filename
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
        # Load the page, it will then do an ajax callback to generate the links
        #
        pass
    else:
        fileList = request.POST.get("selectedFiles")
        if len(fileList) > 0:
            data = json.loads(fileList)
            for record in data:
                _linkfile(record['reference'], getUserName(request))
        else:
            response = render_to_response('500.html', {"message":"No files were selected"},
                                    context_instance=RequestContext(request))
            response.status_code = 500
            return response


    r = _getResources("staging.bundle")

    return render(request, "staging.html", {'jsResources':r})

@csrf_exempt
def stageall(request):
    # get the query used to generate the last result set
    # save the query in the user's session to pull it back out
    # iterate through the results to generate links
    body = request.body.decode('utf-8')

    try:
        postdata = json.loads(body)

    except:
        return JsonResponse({"message":"No/invalid data, original search data could not be parsed", "status":"error"})


    # create links for the entire result set
    fnames = dal.views.get_all_filenames_for_query(postdata)
    stagedfiles = []
    for ref in fnames:
       file = _linkfile(ref, getUserName(request))
       if file:
           stagedfiles.append(file)

    return JsonResponse({'total_files':len(stagedfiles), 'missing_files':missingFiles})


    # get the file list from dal
