from bargainflow.models import Commission, CommissionBid
from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'tags', 'price']

        labels = {
            'title': 'Tytuł',
            'description': 'Opis oferty',
            'tags': 'Tagi',
            'price': 'Cena',
        }

        widgets = {
            'tags': TextInput(attrs={"class" : "tags"}),
        }
        help_texts = {
            'tags': _("Lista tagów oddzielonych przecinkami"),
        }


class CommissionBidForm(forms.ModelForm):
    class Meta:
        model = CommissionBid
        fields = ['bidder_comment', 'commission']

        widgets = {
            'commission': forms.HiddenInput(),
        }
