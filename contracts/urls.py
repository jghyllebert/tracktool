from django.conf.urls import patterns, url

from contracts.views import CreateContract, DetailContract, ListContract, InsertPayment, EditContract


urlpatterns = patterns('',
    url(r'^add/$', CreateContract.as_view(), name='contract_create'),
    url(r'^list/$', ListContract.as_view(), name='contract_list'),
    url(r'^(?P<pk>[0-9]+)/edit/$', EditContract.as_view(), name='contract_edit'),
    url(r'^(?P<pk>[0-9]+)/$', DetailContract.as_view(), name='contract_detail'),
    url(r'^(?P<contract_slug>.*)/payment/$', InsertPayment.as_view(), name='contract_payment'),
)