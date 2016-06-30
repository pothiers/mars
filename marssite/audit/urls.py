from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    #url(r'^$', views.SubmittalList.as_view(), name='submittal_list'),
    url(r'^$', views.AuditRecordList.as_view(), name='sourcefile_list'),
    #url(r'^(?P<pk>[0-9]+)/$', views.SubmittalDetail.as_view(), name='submittal_detail'),
    #url(r'^add$', views.add_submit, name='submittal_add'),
    url(r'^source/$', views.source, name='source'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^refresh/$', views.refresh, name='refresh'),
    url(r'^set_fstop/(?P<md5sum>.+)/(?P<fstop>.+)/$',
        views.set_fstop, name='set_fstop'),
    url(r'^update/$', views.update, name='update'),
    url(r'^missing/$', views.not_ingested, name='not_ingested'),
    url(r'^failed/$', views.failed_ingest, name='failed_ingest'),
    url(r'^notchecknight/$', views.progress_count, name='progress_count'),
    url(r'^progress_plot/$', views.progress, name='progress'),
    url(r'^demo1/$', views.demo_multibarhorizontalchart,  name='demo1'),
    url(r'^hbar/$', views.hbar_svg,  name='hbar_svg'),
    url(r'^dupes/$', views.get_rejected_duplicates,  name='get_rejected_duplicates'),
    url(r'^miss/$', views.get_rejected_missing,  name='get_rejected_missing'),

]


urlpatterns = format_suffix_patterns(urlpatterns)
