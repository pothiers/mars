from django.conf.urls import url

from . import views

urlpatterns = [
    # eg: /siap/
    url(r'^$', views.index, name='index'),
    # eg: /siap/cp243352.fits.gz
    url(r'^(?P<propid>.+)/$', views.filenames, name='filenames'),
]
