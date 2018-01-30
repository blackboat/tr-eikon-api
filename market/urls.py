from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^market/$', views.index, name='index'),
    url(r'^$', views.realtime, name='realtime'),
]