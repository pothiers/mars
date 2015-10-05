from django.conf.urls import url
from . import views


urlpatterns = [
    # eg: /
    url(r'^$', views.home, name='home'),

]
