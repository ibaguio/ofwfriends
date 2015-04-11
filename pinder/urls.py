from django.conf.urls import patterns, include, url
from django.contrib import admin

from pinder import views
admin.autodiscover()

urlpatterns = patterns('pinder',
    # Examples:
    # url(r'^$', 'pinder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/me/$', views.api_me),
    url(r'^api/nearby/$', views.api_people_nearby),
    url(r'^api/search/$', views.api_search),
    url(r'^/$', views.landing_page),
    url(r'^login/', views.test_login),
    url(r'^auth/facebook/$', views.fb_auth_handler, name="fb_auth_handler"),
    url(r'^admin/', include(admin.site.urls)),
)
