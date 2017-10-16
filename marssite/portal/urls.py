from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/?$',
        views.search, name='search'),
    url(r'^stagefiles/?$',
        views.stagefiles, name='stagefiles'),
    url(r'^downloadsinglefile/?$',
        views.downloadsinglefile, name='downloadsinglefile'),
    url(r'^staging/?$',
        views.staging, name='staging'),
]
