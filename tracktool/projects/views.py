from django.contrib.auth.models import Group

from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from project_settings.mixins import SendNotificationMixin

from users.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import Project, ProjectState
from .forms import UpdateFlowForm
from users.models import TrackUser


class DetailProject(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'


class ListProjects(PermissionRequiredMixin, ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 20
    permission_required = 'projects.change_project'

    def dispatch(self, *args, **kwargs):
        """
        Only show list of projects one has access to. Otherwise present them an error
        :param args:
        :param kwargs:
        :return:
        """
        if not self.request.user.is_superuser:
            state_name = self.kwargs.get('state_name')
            if state_name:
                if not self.request.user.groups.filter(name=state_name):
                    raise PermissionDenied
            else:
                group = self.request.user.groups.first()
                return HttpResponseRedirect(reverse('project_list_state', args=[group.name]))
        return super(ListProjects, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        """
        Filter projects based on their current state
        :return:
        """
        queryset = super(ListProjects, self).get_queryset()
        state_name = self.kwargs.get('state_name')
        if state_name:
            queryset = queryset.filter(current_state=state_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListProjects, self). get_context_data(**kwargs)
        #Generate top nav
        queryset = Project.objects.values('current_state').annotate(Count('id'))
        all_that_are_not_finished = Project.objects.exclude(current_state="finished").count()
        context['states'] = queryset
        context['all_that_are_not_finished'] = all_that_are_not_finished

        #Set active display on the right state
        state_name = self.kwargs.get('state_name')
        if state_name:
            context['state_name'] = state_name
        else:
            context['state_name'] = None

        if not self.request.user.is_superuser:
            context['groups'] = self.request.user.groups.all().values_list('name', flat=True)
        else:
            #return all groups
            context['groups'] = Group.objects.all().values_list('name', flat=True)
        return context


class UpdateProjectFlow(PermissionRequiredMixin, SendNotificationMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = UpdateFlowForm
    template_name = 'projects/update.html'
    success_url = reverse_lazy('project_list')
    success_message = "Project updated"
    permission_required = "projects.change_project"

    def form_valid(self, form):
        self.object = form.save()

        if self.object.is_ended:
            #Send project to invoice
            #Only if all projects of contract are done
            all_finished = True
            projects = self.object.contract.project_set.all()
            for p in projects:
                if not p.is_ended:
                    all_finished = False

            if all_finished:
                for project in projects:
                    state = ProjectState(
                        project=project,
                        state="invoicing",
                        user=self.request.user,
                    )
                    state.save()
                projects = self.object.contract.project_set.all()
                projects.update(current_state="invoicing")

                users = []
                for user in TrackUser.objects.filter(groups__name__in=("management", "invoicing")):
                    users.append(user)

                self.send_notification(
                    users=users,
                    message="A contract has been finished by production."
                )

        return super(UpdateProjectFlow, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        if self.object.is_ended:
            self.success_message = "Project sent to invoicing"


class UpdateProjectState(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/update.html'