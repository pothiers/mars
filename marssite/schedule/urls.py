from django.conf.urls import url
from . import views

urlpatterns = [
    # eg: /schedule/
    # The whole schedule
    url(r'^$', views.list, name='list'),

    # eg: /schedule/prop/ct13m/2014-12-25  => smarts
    url(r'^prop/(?P<tele>.+)/(?P<date>.+)/$',
        views.schedprop, name='schedprop'),
]
