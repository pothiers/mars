"""marssite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User # ,Group
from provisional.views import FitsnameViewSet
from schedule.views import ScheduleViewSet


# Serializers define the API representation.
#!class UserSerializer(serializers.HyperlinkedModelSerializer):
#!    class Meta:
#!        model = User
#!        fields = ('url', 'username', 'email', 'is_staff')
#!
#!class GroupSerializer(serializers.HyperlinkedModelSerializer):
#!    class Meta:
#!        model = Group


# ViewSets define the view behavior.
#!class UserViewSet(viewsets.ModelViewSet):
#!    queryset = User.objects.all()
#!    serializer_class = UserSerializer
#!class GroupViewSet(viewsets.ModelViewSet):
#!    queryset = Group.objects.all()
#!    serializer_class = GroupSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#!router.register(r'groups', GroupViewSet)

#router.register(r'fitsnames', FitsnameViewSet)
#router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    url(r'^$', include('water.urls', namespace='water')),
    url(r'^home$', include('water.urls', namespace='water')),

    url(r'^siap/', include('siap.urls', namespace='siap')),
    url(r'^schedule/', include('schedule.urls', namespace='schedule')),
    url(r'^provisional/', include('provisional.urls', namespace='provisional')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls', namespace='docs')),
]
