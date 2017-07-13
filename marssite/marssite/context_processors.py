from django.conf import settings # import the settings file
from os import path

def project_status(request):
    here = path.abspath(path.dirname(path.dirname(__file__)))
    with open(path.join(here,'water','VERSION')) as f:
        version = f.read().strip()
    with open(path.join(here,'water','UPDATED')) as f:
        updated = f.read().strip()

    return {
        'VERSION': version,
        'UPDATED': updated,
        'DBHOST': settings.DATABASES['default']['HOST'],
    }
