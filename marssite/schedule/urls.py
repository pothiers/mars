from django.conf.urls import url
from . import views

urlpatterns = [
    # eg: /schedule/
    # The whole schedule
    url(r'^$', views.list, name='list'),

    # 
    url(r'^empty/$', views.list_empty, name='list_empty'),


    # eg: /schedule/prop/ct13m/2014-12-25/  => smarts
    #  kp4m/2014-01-01 =>  2013B-0142 
    url(r'^propid/(?P<tele>.+)/(?P<date>.+)/$',
        views.getpropid, name='getpropid'),

    url(r'^day/(?P<date>.+)/$',
        views.list_day, name='list_day'),

    #!url(r'^scrape/(?P<begindate>.+)/(?P<enddate>.+)/$',
    #!    views.scrape, name='scrape'),

    url(r'^upload/$',
        views.upload_file, name='upload_file'),
    url(r'^delete_all_schedule_i_really_mean_it/$',
        views.delete_schedule, name='delete_schedule'),
    
]
