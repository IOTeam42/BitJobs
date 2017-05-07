from bargainflow.forms import CommissionForm, CommissionBidForm
from bargainflow.models import Commission, CommissionBid
from moneyflow.models import Customer
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from registration.backends.hmac.views import RegistrationView


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


class CommissionUserView(ListView):
    template_name = "base/commission_user.html"
    model = Commission
    context_object_name = "comm_user"
    paginate_by = 10

    def get_queryset(self):
        queryset = Commission.objects.all()
        pk = self.request.GET.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(Q(orderer=pk))

        return queryset.distinct()


@method_decorator(login_required, name='dispatch')
class CommissionView(DetailView):
    model = Commission
    template_name = "base/commission_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CommissionView, self).get_context_data(**kwargs)
        context['commission_bids'] = context['object'].commission_bids
        commission = self.get_object()
        context['form'] = self._get_commission_bid_form()
        if commission.contractor:
            context['chosen_bid'] = commission.commissionbid_set.get(bidder=commission.contractor)
        return context

    def _get_commission_bid_form(self):
        commission = self.get_object()
        user_bid = commission.commissionbid_set.filter(bidder=self.request.user)
        if user_bid.exists():
            return CommissionBidForm(instance=user_bid.first())
        else:
            return CommissionBidForm(initial={'commission': commission})


def commission_choose(request, pk, bid_id):
    commission = get_object_or_404(Commission, pk=pk)
    commission_bid = get_object_or_404(CommissionBid, pk=bid_id, commission=commission)
    commission.contractor = commission_bid.bidder
    commission.bid = commission_bid
    commission.status = 'A'
    commission.save()
    return redirect('commission-detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class CommissionBidView(FormView):
    form_class = CommissionBidForm

    def __init__(self):
        self.commission = None
        super(CommissionBidView, self).__init__()

    def get_success_url(self):
        return reverse('commission-detail', kwargs={'pk': self.commission.id})

    def form_valid(self, form):
        commission_bid = form.save(commit=False)
        commission_bid.commission.status = 'B'
        commission_bid.bidder = self.request.user
        commission_bid.save()
        self.commission = commission_bid.commission
        return super(CommissionBidView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CommissionAddView(FormView):
    template_name = "base/commission_add.html"
    form_class = CommissionForm

    def __init__(self):
        self.commission = None
        super(CommissionAddView, self).__init__()

    def get_success_url(self):
        return reverse('commission-detail', kwargs={'pk': self.commission.id})

    def form_valid(self, form):
        commission = form.save(commit=False)
        commission.orderer = self.request.user
        commission.contractor = None
        self.request.user.user_ext.wallet.change(commission.price_currency, -commission.price)
        commission.save()
        self.commission = commission
        form.save_m2m()
        return super(CommissionAddView, self).form_valid(form)


def commission_accept_work(request, commission_id):
    commission = get_object_or_404(Commission, pk=commission_id)
    commission.status = 'F'
    commission.contractor.user_ext.wallet.change(commission.price_currency, commission.price)
    commission.save()
    return redirect('commission-detail', pk=commission_id)


class CustomerView(DetailView):
    model = Customer
    template_name = "base/customer_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        return context


class Error500View(TemplateView):
    template_name = "500.html"


class Error403View(TemplateView):
    template_name = "403.html"


class Error404View(TemplateView):
    template_name = "404.html"
