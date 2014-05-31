# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import HomeView, LoginView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    # url(r'^blog/', include('blog.urls')),

)