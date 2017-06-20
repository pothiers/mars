from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'siap', views.SiapViewSet)

urlpatterns = [
    # eg: /dal/
    url(r'^', include(router.urls)),
    url(r'^search/$',
        views.search_by_json, name='search_by_json'),
]
