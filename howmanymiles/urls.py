from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('howmanymiles.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^database/$', 'database', name='database'),
    url(r'^usage/$', TemplateView.as_view(template_name='usage.html'),
        name='usage'),
    url(r'^contribute/$', TemplateView.as_view(template_name='contribute.html'),
        name='contribute'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/', include('howmanymiles.api.urls')),
    url(r'^airline/(?P<pk>\w{2})/$', 'airline_detail', name='airline_detail'),
    url(r'^airline/(?P<earning_pk>\w{2})/(?P<operating_pk>\w{2})/',
        'operating_rules', name='operating_rules'),
    url(r'^rules/(?P<earning_pk>\w{2})/(?P<operating_pk>\w{2})/(?P<fare_class>[A-Z])/',
    'rules_api', name='rules_api'),
)
