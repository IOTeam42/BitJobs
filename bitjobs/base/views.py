from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
    template_name = "base/commission_detail.html"


@method_decorator(login_required, name='dispatch')
class CommissionAddView(FormView):
    template_name = "base/commission_add.html"
    form_class = CommissionForm
    success_url = "/"

    def form_valid(self, form):
        commission = form.save(commit=False)
        commission.orderer = self.request.user
        commission.save()
        form.save_m2m()
        return super(CommissionAddView, self).form_valid(form)


class Error500View(TemplateView):
    template_name = "500.html"


class Error403View(TemplateView):
    template_name = "403.html"


class Error404View(TemplateView):
    template_name = "404.html"
