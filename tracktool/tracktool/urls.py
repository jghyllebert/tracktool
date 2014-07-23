from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from users.views import LoginUser, GetStuffView, LoginView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^client/', include('clients.urls')),
    url(r'^contract/', include('contracts.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^photoshoots/', include('photoshoots.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth_google/', LoginView.as_view(), name="auth_google"),
    url(r'^get_my_stuff/', GetStuffView.as_view(), name='get_my_stuff'),
    url(r'^login/', LoginUser.as_view(), name='user_login'),
    #url(r'^login/', 'users.views.user_login', name='user_login'),
    url(r'^logout/', 'users.views.user_logout', name='user_logout'),
    url(r'$', include('clients.urls')),
)

urlpatterns += staticfiles_urlpatterns()