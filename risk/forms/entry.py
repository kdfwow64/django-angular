"""Forms for auth module."""
from django import forms
from risk.models import Entry


class RiskEntryBasicForm(forms.ModelForm):
    """Form for users to create new Risk Entry."""

    summary = forms.CharField(required=True, min_length=25, max_length=255)
    description = forms.CharField(required=True)
    risk_types = forms.CharField(required=True)
    response = forms.CharField(required=True)
    entry_owner = forms.CharField(required=True)
    aro_fixed = forms.CharField(required=True)
    locations = forms.CharField(required=False)
    compliances = forms.CharField(required=False)
    aro_notes = forms.CharField(required=False)

    class Meta:
        """Meta Class."""

        model = Entry
        fields = ("summary", "description", "risk_types", "response",
                  "locations", "compliances", "aro_fixed", "aro_notes")
