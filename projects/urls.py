from django.conf.urls import patterns, url

from projects.views import DetailProject, ListProjects, UpdateProjectState, UpdateProjectFlow


urlpatterns = patterns('',
    url(r'^list/(?P<state_name>.*)/$', ListProjects.as_view(), name='project_list_state'),
    url(r'^list/$', ListProjects.as_view(), name='project_list'),
    url(r'^(?P<pk>[0-9]+)/state/$', UpdateProjectState.as_view(), name='project_state'),
    url(r'^(?P<pk>[0-9]+)/todo/$', UpdateProjectFlow.as_view(), name='project_update_flow'),
    url(r'^(?P<pk>[0-9]+)/$', DetailProject.as_view(), name='project_detail'),
)

