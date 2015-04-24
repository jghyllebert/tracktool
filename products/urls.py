from django.conf.urls import patterns, url

from products.views import ApiProductOptions


urlpatterns = patterns('',
    #url(r'^add/$', CreateContract.as_view(), name='contract_create'),
    #url(r'^list/$', ListContract.as_view(), name='contract_list'),
    #url(r'^(?P<pk>[0-9]+)/$', DetailContract.as_view(), name='contract_detail'),
    url(r'^api/get_options/(?P<pk>[0-9]+)/$', ApiProductOptions.as_view(), name="product_api_options"),
)