from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from bargainflow.models import Commission


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['description', 'tags']

        widgets = {
            'tags': TextInput(attrs={"class" : "tags"}),
        }
        help_texts = {
            'tags': _("Comma separated list of tags"),
        }
