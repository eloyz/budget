import os
from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', include('homepage.urls')),
	(r'^time-spent/', include('time_spent.urls')),
	(r'^accounts/', include('registration.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

try:
    from local_urls import extra_patterns
    urlpatterns += extra_patterns
except ImportError:
    pass