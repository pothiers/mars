from django.conf.urls import url

from . import views

urlpatterns = [
    # eg: /siap/
    url(r'^$', views.index, name='index'),

    # eg: /siap/prop/2011A-0525
    url(r'^prop/(?P<propid>.+)/$', views.filenames, name='filenames'),
    # eg: /siap/detail/cp243352.fits.gz
    url(r'^detail/(?P<image_id>.+)/$', views.detail, name='detail'),
]
