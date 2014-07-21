import httplib2
from datetime import datetime
from apiclient.discovery import build
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy

from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from clients.forms import ClientAddForm
from clients.models import ContactPerson
from .forms import ContractForm, ContractProjectsFormSet, UpdatePaymentForm, UpdateContractForm
from .models import Contract, Payment
from project_settings.mixins import SendNotificationMixin
from projects.models import ProjectState
from users.forms import ClientContactForm
from users.mixins import LoginRequiredMixin, PermissionRequiredMixin
from users.models import TrackUser


class CreateContract(LoginRequiredMixin, PermissionRequiredMixin, SendNotificationMixin, CreateView):
    template_name = 'contracts/create.html'
    model = Contract
    form_class = ContractForm
    permission_required = 'contracts.add_contract'

    def get_context_data(self, **kwargs):
        context = super(CreateContract, self).get_context_data(**kwargs)

        if self.request.POST:
            context['contractproject_form'] = ContractProjectsFormSet(self.request.POST)
            existing_client = self.request.POST.get('existing_client')
            if existing_client != "on":
                context['new_client_form'] = ClientAddForm(self.request.POST)
                context['client_contact_form'] = ClientContactForm(self.request.POST)
        else:
            context['contractproject_form'] = ContractProjectsFormSet()
            context['new_client_form'] = ClientAddForm()
            context['client_contact_form'] = ClientContactForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        contractproject_form = context['contractproject_form']

        existing_client = self.request.POST.get('existing_client')
        if existing_client != "on":
            client_contact_form = context['client_contact_form']
            new_client_form = context['new_client_form']

            if new_client_form.is_valid() and client_contact_form.is_valid() and contractproject_form.is_valid():
                new_client_form.instance.account_manager = self.request.user
                client = new_client_form.save()
                role = self.request.POST["role"]
                notes = self.request.POST["notes"]
                client_contact = client_contact_form.save()

                # Create a new contact
                contact_person = ContactPerson(
                    client=client,
                    user=client_contact,
                    role=role,
                    notes=notes
                )
                contact_person.save()
                self.object = form.save(commit=False)
                self.object.client = client
                self.object.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

        if contractproject_form.is_valid():
            if existing_client:
                self.object = form.save()

            contractproject_form.instance = self.object
            contractproject_form.save()

            # add options
            projects = self.object.project_set.all()
            for project in projects:
                product = project.product
                options = self.request.POST.getlist(product.slug + "_option")
                flow = product.flow.splitlines()
                position = flow.index("-- INSERT OPTIONS --")
                for option in options:
                    #insert options after --INSERT OPTIONS
                    flow.insert(position + 1, option)
                #Remove -- INSERT OPTION --
                flow.pop(position)

                #Convert back to TextField
                workflow = ""
                for todo in flow:
                    workflow += todo + "\n"
                project.flow = workflow
                project.save()

                #Create states
                state = ProjectState(
                    project=project,
                    user=self.request.user,
                    notes="Sales created contract",
                )
                state.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        users = []
        for user in TrackUser.objects.filter(groups__name__in=("management",)):
            users.append(user)

        self.send_notification(
            message="%(user)s created a contract" % {'user': self.request.user.get_full_name()},
            users=users,
        )

        """
        Create folders on Google drive
        """
        file_user = TrackUser.objects.get(pk=2)
        drive_service = build('drive', 'v2', http=file_user.credentials.authorize(httplib2.Http()))
        folder_body = {
            "title": "%(contract)d-%(client)s-%(city)s" % {
                "contract": self.object.contract_number,
                "client": self.object.client,
                "city": self.object.shoot_city
            },
            "parents": [{"id": self.object.client.country.drive_folder_id}],
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = drive_service.files().insert(body=folder_body).execute()

        #Save folder in Contract
        self.object.drive_folder_id = folder['id']
        self.object.save()

        sub_folders = ['Combi', 'Compressed', 'Other', 'Panos', 'Poi']
        for sub_folder in sub_folders:
            sub_folder_body = {
                "title": sub_folder,
                "parents": [{"id": folder['id']}],
                "mimeType": "application/vnd.google-apps.folder"
            }
            drive_service.files().insert(body=sub_folder_body).execute()

        return super(CreateContract, self).form_valid(form)


class DetailContract(LoginRequiredMixin, DetailView):
    model = Contract
    template_name = 'contracts/detail.html'
    context_object_name = 'contract'


class EditContract(UpdateView):
    model = Contract
    template_name = 'contracts/edit.html'
    form_class = UpdateContractForm

    def dispatch(self, *args, **kwargs):
        """
        Only sales can edit their own contracts (and superusers too)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not self.request.user.is_superuser:
            if self.object.client.account_manager != self.request.user:
                raise PermissionDenied
        return super(EditContract, self).dispatch(*args, **kwargs)


class ListContract(LoginRequiredMixin, ListView):
    model = Contract
    context_object_name = 'contracts'
    template_name = 'contracts/list.html'


class InsertPayment(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, SendNotificationMixin,
                    CreateView):
    model = Payment
    form_class = UpdatePaymentForm
    template_name = "photoshoots/create.html"
    success_url = reverse_lazy('contract_list')
    success_message = "Inserted payment"

    def get_context_data(self, **kwargs):
        context = super(InsertPayment, self).get_context_data(**kwargs)
        parent = Contract.objects.get(slug=self.kwargs['contract_slug'])
        context['contract'] = parent
        return context

    def get_initial(self):
        contract = Contract.objects.get(slug=self.kwargs['contract_slug'])
        return {'contract': contract, 'inputter': self.request.user}

    def form_valid(self, form):
        self.object = form.save()

        # Update amount paid
        self.object.contract.amount_paid += self.object.amount

        #Check if total amount due is fulfilled
        if self.object.contract.amount_paid >= self.object.contract.total_cost:
            self.object.contract.is_paid = True
            self.object.contract.date_is_paid = datetime.now

            users = []
            for user in TrackUser.objects.filter(groups__name__in=("management",)):
                users.append(user)

            self.send_notification(
                users=users,
                message="A Contract has been fully paid.",
            )

            self.object.contract.project_set.all().update(current_state="finished")
            for project in self.object.contract.project_set.all():
                state = ProjectState(
                    project=project,
                    state="production",
                    user=self.request.user,
                )
                state.save()

        self.object.contract.save()

        return super(InsertPayment, self).form_valid(form)