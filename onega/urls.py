from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.shortcuts import HttpResponse

from chips.forms import ThemedPasswordResetForm, ThemedSetPasswordForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'onega.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('chips.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name="auth_logout"),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/password/reset/done/', 'template_name': 'registration/password_reset.html',
         'password_reset_form': ThemedPasswordResetForm},
        name="password_reset"),
    (r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done',
     {'template_name': 'registration/password_reset_done.html'}),
    (r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/password/done/', 'template_name': 'registration/password_reset_confirm.html',
        'set_password_form': ThemedSetPasswordForm}),
    (r'^password/done/$', 'django.contrib.auth.views.password_reset_complete',
     {'template_name': 'registration/password_reset_complete.html'}),
)

urlpatterns += patterns('',
    url(r'^robots\.txt$',
        lambda r: HttpResponse(
            "User-agent: *\nDisallow: /admin\nDisallow: /profile",
            mimetype="text/plain"))
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
