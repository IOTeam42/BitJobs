from django import forms
from bargainflow.models import Commission


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = '__all__'
