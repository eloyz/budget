from django.conf.urls.defaults import *

urlpatterns = patterns('time_spent',
    url(r'^$', 'views.detail', name="time-spent"),
    url(r'^income/$', 'views.income', name="income"),
    url(r'^expenses/$', 'views.expenses', name="expenses"),
    url(r'^net-income/$', 'views.net_income', name="net-income"),
    url(r'^wish/$', 'views.wish', name="wish"),
    url(r'^wish/change/(?P<pk>\d+)$', 'views.wish_change', name="wish-change"),
    url(r'^wish/remove/(?P<pk>\d+)$', 'views.wish_remove', name="wish-remove"),
    url(r'^(?P<month>\d{1,2})/(?P<year>\d{4})/$', 'views.detail', name="time-spent"),
)
