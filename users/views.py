from apiclient.discovery import build
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import ListView
import httplib2
from oauth2client.client import OAuth2WebServerFlow

from users.forms import UserForm, LoginForm
from users.models import TrackUser
from users.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CreateSales(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TrackUser
    template_name = 'users/create.html'
    form_class = UserForm
    permission_required = 'add_trackuser'

    def form_valid(self, form):
        response = super(CreateSales, self).form_valid(form)
        self.object.groups.add(Group.objects.get(name="sales"))


class ListSales(LoginRequiredMixin, ListView):
    model = TrackUser
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return TrackUser.objects.filter(groups__name="sales")

    def get_context_data(self, **kwargs):
        context = super(ListSales, self).get_context_data(**kwargs)
        context['title'] = 'Sales'
        return context


class ListUsers(LoginRequiredMixin, ListView):
    model = TrackUser
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super(ListUsers, self).get_context_data(**kwargs)
        context['title'] = 'Users'


class DetailUser(LoginRequiredMixin, DetailView,):
    model = TrackUser
    template_name = 'users/detail.html'
    context_object_name = 'track_user'


class UpdateUser(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    model = TrackUser
    template_name = 'users/create.html'
    success_message = "%(user)s successfully updated"

    def get_success_message(self, cleaned_data):
        return self.success_message % {}


class DeleteUser(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
    model = TrackUser
    template_name = 'users/delete.html'
    context_object_name = 'track_user'
    success_message = "User deleted!"

    def get_success_url(self):
        return reverse('user_list_sales')

    def delete(self, request, *args, **kwargs):
        """
        SuccessMessageMixin doesn't work with DeleteView yet. So, override delete function
        Let it stay for future, a fix is on the way https://code.djangoproject.com/ticket/21936
        """
        response = super(DeleteUser, self).delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response


def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            if user.groups.filter(name="sales").exists():
                return HttpResponseRedirect(reverse('contract_create'))
            else:
                return HttpResponseRedirect(reverse('home'))

    return render(request, 'users/login.html', {
    })


class LoginUser(FormView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

        if user is not None:
            login(self.request, user)
            next_url = self.request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            if user.groups.filter(name="sales").exists():
                self.success_url = reverse_lazy('contract_create')
        else:
            return self.form_invalid(form)
        return super(LoginUser, self).form_valid(form)


def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('user_login'))


#### Google Auth
class LoginView(TemplateView):
    template_name = "users/step1.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        flow = OAuth2WebServerFlow(settings.GOOGLE_CLIENT, settings.GOOGLE_SECRET, settings.OAUTH_SCOPE,
                                   settings.REDIRECT_URL)
        flow.params['access_type'] = 'offline'
        flow.params['approval_prompt'] = 'force'
        authorize_url = flow.step1_get_authorize_url()
        context['authorize_url'] = authorize_url

        return context


class GetStuffView(TemplateView):
    template_name = "users/step2.html"

    def dispatch(self, request, *args, **kwargs):
        google_code = self.request.GET.get('code')

        if not google_code:
            raise PermissionDenied
        return super(GetStuffView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GetStuffView, self).get_context_data(**kwargs)
        # we already check that code existed in dispatch
        google_code = self.request.GET.get('code')
        flow = OAuth2WebServerFlow(settings.GOOGLE_CLIENT, settings.GOOGLE_SECRET, settings.OAUTH_SCOPE,
                                   settings.REDIRECT_URL)
        credentials = flow.step2_exchange(google_code)
        context['credentials'] = credentials

        #Save credentials
        user = self.request.user
        user.credentials = credentials
        user.save()

        user_info_service = build(
            serviceName='oauth2', version='v2',
            http=credentials.authorize(httplib2.Http()))

        user_info = user_info_service.userinfo().get().execute()
        if user_info and user_info.get('id'):
            context['user_info'] = user_info

        return context