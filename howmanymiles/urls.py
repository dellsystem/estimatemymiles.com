from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'howmanymiles.views.home', name='home'),
    url(r'^progress/$', 'howmanymiles.views.progress', name='progress'),
    url(r'^progress/(?P<operating>\w{2})/(?P<earning>\w{2})/$',
        'howmanymiles.views.progress_detail', name='progress_detail'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^usage/$', TemplateView.as_view(template_name='usage.html'),
        name='usage'),
    url(r'^contribute/$', TemplateView.as_view(template_name='contribute.html'),
        name='contribute'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('howmanymiles.api.urls')),
)
