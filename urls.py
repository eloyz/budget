from django.conf.urls.defaults import patterns, include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', include('homepage.urls')),
    (r'^time-spent/', include('time_spent.urls')),
    (r'^post-recieve/', include('post_recieve.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

try:
    from local_urls import extra_patterns
    urlpatterns += extra_patterns
except ImportError:
    pass
