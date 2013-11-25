from django.conf.urls import patterns, include, url


urlpatterns = patterns('howmanymiles.api.views',
    url('fareclasses/(?P<airline_pk>\w{2})/', 'fareclasses'),
    url('mileages/(?P<fareclass_pk>\d+)/', 'mileages'),
)
