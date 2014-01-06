from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('howmanymiles.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^usage/$', TemplateView.as_view(template_name='usage.html'),
        name='usage'),
    url(r'^contribute/$', TemplateView.as_view(template_name='contribute.html'),
        name='contribute'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/', include('howmanymiles.api.urls')),
    url(r'^airline/(?P<pk>\w{2})/$', 'airline_detail', name='airline_detail')
)
