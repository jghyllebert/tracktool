from django.conf.urls import patterns, url

from photoshoots.views import CreatePhotoshootAppointment, ListPhotoshoots, PhotoshootDoneView


urlpatterns = patterns('',
    url(r'^add/(?P<contract_slug>.*)/$', CreatePhotoshootAppointment.as_view(), name='photoshoot_create'),
    url(r'^list/$', ListPhotoshoots.as_view(), name='photoshoot_list'),
    url(r'^complete/(?P<contract_slug>.*)/(?P<pk>[0-9]+)/$', PhotoshootDoneView.as_view(), name='photoshoot_done'),
    #url(r'^(?P<pk>[0-9]+)/$', DetailClient.as_view(), name='client_detail'),
    #url(r'$', ListClient.as_view(), name='home'),
)