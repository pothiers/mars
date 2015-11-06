from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # eg: /schedule/
    # The whole schedule
    url(r'^$', views.list, name='list'),
    url(r'^list/$', views.SlotList.as_view(), name='list'),
    #!url(r'^$', views.SlotList.as_view(), name='list'),
    #!url(r'^$', views.api_root, name='api_root'),

    url(r'^about/$',
        TemplateView.as_view(template_name="schedule/about.html")),
    
    url(r'^empty/$', views.list_empty, name='list_empty'),

    url(r'^today$', views.SlotTodayList.as_view(), name='today_list'),

     # By Month;  Example: /2012/aug/
     url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
         views.SlotMonthList.as_view(),
         name="month_list"),
    #! # Example: /2012/08/
    #! url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
    #!     views.SlotMonthList.as_view(month_format='%m'),
    #!     name="month_numeric_list"),
    #! # By Week; Example: /2012/week/23/
    #! url(r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$', 
    #!     views.SlotWeekList.as_view(),
    #!     name='week_list'),
    #! # By Day;  Example: /2012/nov/10/
    #! url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$',
    #!     views.SlotDayList.as_view(),
    #!     name="day_list"),

    # eg: /schedule/propid/ct13m/2014-12-25/  => smarts
    #  kp4m/2014-01-01 =>  2013B-0142 
    url(r'^propid/(?P<tele>.+)/(?P<date>.+)/$',
        views.getpropid, name='getpropid'),
    url(r'^slot/(?P<tele>.+)/(?P<date>.+)/$',
        views.SlotGet.as_view(), name='getslot'),

    #!url(r'^day/(?P<date>.+)/$', views.list_day, name='list_day'),

    #!url(r'^scrape/(?P<begindate>.+)/(?P<enddate>.+)/$',
    #!    views.scrape, name='scrape'),

    url(r'^upload/$',
        views.upload_file, name='upload_file'),
    url(r'^delete_all_schedule_i_really_mean_it/$',
        views.delete_schedule, name='delete_schedule'),
    
]

