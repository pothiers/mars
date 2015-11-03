from django.conf.urls import url
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    # eg: /provisional/
    url(r'^$', views.index, name='index'),
    url(r'^about/$',
        TemplateView.as_view(template_name="provisional/about.html")),

    url(r'^list/$', views.ProvListView.as_view(), name='prov-list'),

    # eg: /provisional/stuff/
    url(r'^stuff/$',
        views.stuff_with_tada, name='stuff'),
    # eg: /provisional/add/kp1794587.fits.fz/
    url(r'^add/(?P<reference>.+)/$',
        views.add, name='add'),
    url(r'^delete/(?P<reference>.+)/$',
        views.dbdelete, name='delete'),
    url(r'^rollback/$',
        views.rollback, name='rollback'),

]
