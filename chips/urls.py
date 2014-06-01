# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import HomeView, ProfileView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^home/$', HomeView.as_view()),
    url(r'^home/(?P<method>\w+)/$', HomeView.as_view(), name='post_form_home'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),

    # url(r'^blog/', include('blog.urls')),

)