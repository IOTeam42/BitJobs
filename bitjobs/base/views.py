from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User

from registration.backends.hmac.views import RegistrationView
from registration.signals import user_registered

from bargainflow.models import Commission
from bargainflow.forms import CommissionForm


class RegisterView(RegistrationView):
    success_url = "/"


class LoginView(TemplateView):
    template_name = "registration/login.html"


class HomeView(TemplateView):
    template_name = "base/main.html"


class CommissionDashboardView(ListView):
    template_name = "base/commission_list.html"
    model = Commission
    context_object_name = "comm_list"
    paginate_by = 10


class CommissionView(DetailView):
    model = Commission


class CommissionAddView(TemplateView):
    template_name = "base/commission_add.html"

    def get_context_data(self, **kwargs):
        context = super(CommissionAddView, self).get_context_data(**kwargs)
        context['form'] = CommissionForm()
        return context
