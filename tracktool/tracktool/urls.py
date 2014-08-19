from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

from users.views import LoginUser, GetStuffView, LoginView
from tastypie.api import Api
from rest.api import ClientResource

admin.autodiscover()

v1_api = Api(api_name="v1")
v1_api.register(ClientResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
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
    url(r'', TemplateView.as_view(template_name='clients/list.html')),
)

urlpatterns += staticfiles_urlpatterns()