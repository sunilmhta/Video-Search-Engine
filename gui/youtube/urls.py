from django.conf.urls import  include, url
from django.contrib import admin
from django.conf import settings

from . import views

app_name='youtube'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^submit/$',views.submit,name='submit'),
    url(r'^neo/(?P<neo_data>[0-9A-Za-z_-]+)/$',views.neo,name='neo'),
    url(r'^watch/(?P<video_id>[0-9A-Za-z_-]+)/$', views.watch,name='watch' ),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^checklogin/$',views.checklogin,name='checklogin'),
    url(r'^thanks/$',views.thanks,name='thanks'),
    url(r'^history/$',views.history,name='history'),
    url(r'$',views.index,name='index'),
]