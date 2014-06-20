# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import HomeView, ProfileView, LogoutView, Prize

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^home/$', HomeView.as_view(), name='another_home'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^home/(?P<method>\w+)/$', HomeView.as_view(), name='post_form_home'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^prize/$', Prize.as_view(), name='prize'),
)