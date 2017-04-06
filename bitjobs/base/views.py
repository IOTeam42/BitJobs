from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from bargainflow.models import Commission
from bargainflow.forms import CommissionForm


class RegisterView(TemplateView):
    template_name = "base/templates/registration/registration.html"


class LoginView(TemplateView):
    template_name = "base/templates/registration/login.html"


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
        context['commission-form'] = CommissionForm()
