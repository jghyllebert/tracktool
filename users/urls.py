from django.conf.urls import patterns, url

from users.views import UpdateUser
from users.views import CreateSales, ListSales, DetailUser, DeleteUser, LoginView


urlpatterns = patterns('',
    url(r'^sales/add/$', CreateSales.as_view(), name='user_create_sales'),
    url(r'^google/$', LoginView.as_view(), name='user_google'),
    url(r'^list/$', ListSales.as_view(), name='user_list_sales'),
    url(r'^edit/(?P<pk>[0-9]+)/$', UpdateUser.as_view(), name='user_update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', DeleteUser.as_view(), name='user_delete'),
    url(r'^(?P<pk>[0-9]+)/$', DetailUser.as_view(), name='user_detail'),
)