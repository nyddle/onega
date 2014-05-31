# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import HomeView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^home/(?P<method>\w+)/$', HomeView.as_view(), name='post_form_home'),
    # url(r'^login/$', LoginView.as_view(), name='login'),

    # url(r'^blog/', include('blog.urls')),

)