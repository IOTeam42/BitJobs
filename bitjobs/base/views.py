from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from registration.backends.hmac.views import RegistrationView

from bargainflow.models import Commission
from bargainflow.forms import CommissionForm, CommissionBidForm


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

    def get_queryset(self):
        queryset = Commission.objects.all()
        desc = self.request.GET.get('desc', None)

        if desc is not None:
            queryset = queryset.filter(Q(description__icontains=desc) |
                                       Q(title__iexact=desc) |
                                       Q(tags__name__in=[desc]))

        return queryset.distinct()


class CommissionView(DetailView):
    model = Commission
    template_name = "base/commission_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CommissionView, self).get_context_data(**kwargs)
        context['commission_bids'] = context['object'].commission_bids
        context['form'] = CommissionBidForm(initial={'commission': context['object']})
        return context


@method_decorator(login_required, name='dispatch')
class CommissionBidView(FormView):
    form_class = CommissionBidForm
    success_url = "/"

    def form_valid(self, form):
        commission_bid = form.save(commit=False)
        commission_bid.bidder = self.request.user
        commission_bid.save()
        return super(CommissionBidView, self).form_valid(form)


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
