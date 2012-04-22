from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('post_recieve.views', 
    url(r'^$', 'details', name="post-recieve"),
)