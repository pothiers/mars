import pathlib
from django.apps import apps
from django.core import management

my_apps = [
    'audit',
    'provisional',
    'schedule',
    'siap',
    'tada',
    'water',
    ]


#! for my_app in my_apps:
#!     for c in apps.get_app_config(my_app).get_models():
#!         print('app.model='.format(my_app, c.__name__))


def dump_my_apps(dir, apps=my_apps):
    for myapp in apps:
        outpath = pathlib.PurePath(dir, myapp+'.yaml')
        print('dump django models to: {}', str(outpath))
        management.call_command('dumpdata', myapp,
                                '--format=yaml',
                                '--indent=4',
                                '--output={}'.format(str(outpath)),
        )

        
