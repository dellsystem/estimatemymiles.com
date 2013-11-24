from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^howmanymiles/', include('howmanymiles.foo.urls')),

    url(r'^$', 'howmanymiles.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
