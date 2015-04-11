from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('ofwfriends',
    # Examples:
    # url(r'^$', 'ofwfriends.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'/', views.landing_page),
    url(r'^auth/facebook/$', views.fb_auth_handler, name="fb_auth_handler"),
    url(r'^admin/', include(admin.site.urls)),
)
