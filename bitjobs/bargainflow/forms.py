from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from bargainflow.models import Commission, CommissionBid


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'tags']

        widgets = {
            'tags': TextInput(attrs={"class" : "tags"}),
        }
        help_texts = {
            'tags': _("Comma separated list of tags"),
        }


class CommissionBidForm(forms.ModelForm):
    class Meta:
        model = CommissionBid
        fields = ['bidder_comment', 'commission']

        widgets = {
            'commission': forms.HiddenInput(),
        }
