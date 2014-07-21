from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import ClientAddForm
from .models import Client, ContactPerson
from users.forms import ClientContactForm
from users.mixins import LoginRequiredMixin


class CreateClient(LoginRequiredMixin, CreateView):
    template_name = 'clients/create_client.html'
    model = Client
    form_class = ClientAddForm

    def get_context_data(self, **kwargs):
        context = super(CreateClient, self).get_context_data(**kwargs)

        if self.request.POST:
            context['client_contact_form'] = ClientContactForm(self.request.POST)
        else:
            context['client_contact_form'] = ClientContactForm()
        return context

    def form_valid(self, form):
        form.instance.account_manager = self.request.user

        context = self.get_context_data()
        client_contact_form = context['client_contact_form']
        if client_contact_form.is_valid():
            self.object = form.save()
            role = self.request.POST['role']
            notes = self.request.POST['notes']
            client_contact = client_contact_form.save()

            #Create a new contact
            contact_person = ContactPerson(
                client=self.object,
                user=client_contact,
                role=role,
                notes=notes,
            )
            contact_person.save()

        return super(CreateClient, self).form_valid(form)


class DetailClient(LoginRequiredMixin, DetailView):
    template_name = 'clients/detail.html'
    model = Client
    context_object_name = 'client'


class ListClient(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = 'clients'
    template_name = 'clients/list.html'


class EditClient(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'clients/edit.html'
    form = ClientAddForm

    def dispatch(self, *args, **kwargs):
        """
        Sales can only edit their own clients
        :param args:
        :param kwargs:
        :return:
        """
        if not self.request.user.is_superuser:
            if self.object.account_manager != self.request.user:
                raise PermissionDenied
        return super(EditClient, self).dispatch(*args, **kwargs)