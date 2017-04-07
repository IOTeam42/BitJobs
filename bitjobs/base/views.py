from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User

from registration.views import RegistrationView
from registration.signals import user_registered

from bargainflow.models import Commission
from bargainflow.forms import CommissionForm


class RegisterView(RegistrationView):

    success_url = "/"

    def register(self, form):
        data = form.cleaned_data
        username = data['username']
        password = data['password1']
        email = data['email']
        user = User.objects.create_user(username, email, password)
        return user


class LoginView(TemplateView):
    template_name = "registration/login.html"


class HomeView(TemplateView):
    template_name = "base/main.html"


class CommissionDashboardView(ListView):
    model = Commission


class CommissionView(DetailView):
    model = Commission


class CommissionAddView(TemplateView):
    template_name = "base/commission_add.html"

    def get_context_data(self, **kwargs):
        context = super(CommissionAddView, self).get_context_data(**kwargs)
        context['form'] = CommissionForm()
        return context
