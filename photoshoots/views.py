from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.utils import timezone

from contracts.models import Contract
from photoshoots.models import PhotoshootAppointment
from photoshoots.forms import CreateAppointment, PhotoShootComplete
from project_settings.mixins import SendNotificationMixin
from projects.models import ProjectState, Project
from users.mixins import LoginRequiredMixin
from users.models import TrackUser


class PhotoshootContractMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PhotoshootContractMixin, self).get_context_data(**kwargs)
        parent = Contract.objects.get(slug=self.kwargs['contract_slug'])
        context['contract'] = parent
        #Set current time zone to that of the client
        timezone.activate(parent.client.country.timezone)
        return context

    def get_initial(self):
        """
        Copy description from projects given by sales
        :return:
        """
        parent = Contract.objects.get(slug=self.kwargs['contract_slug'])
        projects = parent.project_set.all()
        description = ""

        for project in projects:
            description += "%(product)s\n%(description)s\n\n" % {
                'product': project.product.name,
                'description': project.notes,
            }

        return {'description': description}


class CreatePhotoshootAppointment(LoginRequiredMixin, SuccessMessageMixin, SendNotificationMixin, PhotoshootContractMixin, CreateView):
    model = PhotoshootAppointment
    form_class = CreateAppointment
    template_name = 'photoshoots/create.html'
    success_message = "Photoshoot saved"
    success_url = reverse_lazy("photoshoot_list")

    def form_valid(self, form):
        context = self.get_context_data()
        contract = context['contract']

        appointment = form.save()
        appointment.contract = contract
        appointment.created_by = self.request.user
        appointment.save()

        #Update states
        projects = contract.project_set.all()
        for project in projects:
            state = ProjectState(
                project=project,
                state="photographer",
                user=self.request.user,
            )
            state.save()
        projects.update(current_state="photographer")

        #Notifications
        users = []
        for user in TrackUser.objects.filter(groups__name__in=("management",)):
            users.append(user)

        #Photographer
        users.append(appointment.photographer)

        self.send_notification(
            message="%(user)s created a new appointment" % {'user': self.request.user.get_full_name()},
            users=users,
        )

        return super(PhotoshootContractMixin, self).form_valid(form)


class ListPhotoshoots(LoginRequiredMixin, ListView):
    model = PhotoshootAppointment
    template_name = "photoshoots/list.html"
    context_object_name = "shoots"

    def get_queryset(self):
        projects = Project.objects.filter(current_state="photographer")
        return PhotoshootAppointment.objects.filter(contract__in=projects.values('contract'))


class PhotoshootDoneView(LoginRequiredMixin, PhotoshootContractMixin, SendNotificationMixin, SuccessMessageMixin, UpdateView):
    model = PhotoshootAppointment
    form_class = PhotoShootComplete
    template_name = "photoshoots/done.html"
    success_url = reverse_lazy("photoshoot_list")
    success_message = "Shoot successfully sent to production"

    def form_valid(self, form):
        context = self.get_context_data()
        contract = context['contract']

        #Shoot is over --> set to inactive
        self.object = form.save()
        self.object.active = False
        self.object.save()

        #Update states
        projects = contract.project_set.all()
        for project in projects:
            state = ProjectState(
                project=project,
                state="production",
                user=self.request.user,
            )
            state.save()
        projects.update(current_state="production", notes=self.request.POST['description'])

        #Notifications
        users = []
        for user in TrackUser.objects.filter(groups__name__in=("management", "production")):
            users.append(user)

        self.send_notification(
            message="%(user)s uploaded pictures for contract %(contract)d" % {
                'user': self.object.photographer,
                'contract': self.object.contract.contract_number,
            },
            users=users,
        )

        return super(PhotoshootDoneView, self).form_valid(form)
