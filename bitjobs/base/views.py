from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from bargainflow.models import Commission


class RegisterView(TemplateView):
    template_name = "base/templates/registration/registration.html"

    def get_context_data(self, **kwargs):
        super(RegisterView).__init__(**kwargs)


class LoginView(TemplateView):
    template_name = "base/templates/registration/login.html"

    def get_context_data(self, **kwargs):
        super(LoginView).__init__(**kwargs)


class HomeView(TemplateView):
    template_name = "base/main.html"


class CommissionDashboardView(ListView):
    model = Commission


class CommissionView(DetailView):
    model = Commission
