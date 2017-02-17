from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pfx$', views.prefix, name='prefix'),
    url(r'^obs$', views.obstype, name='obstype'),
    url(r'^proc$', views.proctype, name='proctype'),
    url(r'^prod$', views.prodtype, name='prodtype'),

]
