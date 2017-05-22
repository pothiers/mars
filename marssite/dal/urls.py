from django.conf.urls import url
from . import views

urlpatterns = [
    # eg: /dal/
    #! url(r'^$', views.index, name='index'),

    url(r'^search/$', views.search_by_json, name='search_by_json'),
]
