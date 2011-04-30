from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'html5musicplay.player.views.home', name='home'),
     url(r'^getFiles$', 'html5musicplay.player.views.getFiles'),
     
     #(r'^music/(?P<path>.*)$', 'django.views.static.serve',
      #  {'document_root': settings.MUSIC_ROOT}),
     url(r'^music/(?P<filepath>.*)$', 'html5musicplay.player.views.fileConverter'),
     (r'^css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.CSS_ROOT}),
    # url(r'^html5musicplay/', include('html5musicplay.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
