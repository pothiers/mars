from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/?$',
        views.search, name='search'),
    url(r'^downloadselected/?$',
        views.downloadselected, name='downloadselected'),
    url(r'^downloadsinglefile/?$',
        views.downloadsinglefile, name='downloadsinglefile'),
    url(r'^staging/?$',
        views.staging, name='staging'),
]
