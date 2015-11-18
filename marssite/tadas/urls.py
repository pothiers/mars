from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^$', views.SubmittalList.as_view(), name='submittal_list'),
    url(r'^(?P<pk>[0-9]+)/$',
        views.SubmittalDetail.as_view(),  name='submittal_detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
