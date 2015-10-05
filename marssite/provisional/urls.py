from . import views


urlpatterns = [
    # eg: /provisional/
    url(r'^$', views.index, name='index'),

 
    # eg: /siap/get/nsa/local_filename.fits
    url(r'^insert/(?P<dtacqnam>.+)/(?P<dtnsanam>.+)/$',
        views.insert, name='insert'),
]
