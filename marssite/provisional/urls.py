from django.conf.urls import url

from . import views


urlpatterns = [
    # eg: /provisional/
    url(r'^$', views.index, name='index'),

 
    # eg: /siap/get/nsa/local_filename.fits
    url(r'^add/(?P<reference>.+)/$',
        views.add, name='add'),

    url(r'^delete/(?P<reference>.+)/$',
        views.dbdelete, name='delete'),
]
