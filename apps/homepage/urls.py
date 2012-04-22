from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('homepage.views', 
    url(r'^$', 'details', name="homepage"),
)