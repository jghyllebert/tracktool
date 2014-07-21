from django.conf.urls import patterns, url

from .views import CreateClient, DetailClient, ListClient, EditClient


urlpatterns = patterns('',
    url(r'^add/$', CreateClient.as_view(), name='client_create'),
    url(r'^list/$', ListClient.as_view(), name='client_list'),
    url(r'^(?P<pk>[0-9]+)/edit/$', EditClient.as_view(), name='client_edit'),
    url(r'^(?P<pk>[0-9]+)/$', DetailClient.as_view(), name='client_detail'),
    url(r'$', ListClient.as_view(), name='home'),
)