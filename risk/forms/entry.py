"""Forms for auth module."""
from django import forms
from risk.models import Entry, Response


class RiskEntryBasicForm(forms.ModelForm):
    """Form for users to create new Risk Entry."""

    summary = forms.CharField(required=True, min_length=25, max_length=255)
    description = forms.CharField(required=True)
    assumption = forms.CharField(required=True)
    locations = forms.CharField(required=False)
    response = forms.CharField(required=True)
    # risk_types = forms.CharField(required=False)
    # response = forms.ModelChoiceField(
    #     queryset=Response.objects.all(), required=True)
    entry_owner = forms.CharField(required=True)
    evaluation_days = forms.CharField(required=True)
    aro_known_multiplier = forms.CharField(required=False)
    aro_known_unit_quantity = forms.CharField(required=False)
    aro_toggle = forms.CharField(required=False)
    aro_time_unit = forms.CharField(required=False)
    aro_frequency = forms.CharField(required=False)
    aro_fixed = forms.CharField(required=False)
    aro_notes = forms.CharField(required=False)

    compliance_requirements = forms.CharField(required=False)
    entry_urls = forms.CharField(required=False)
    incident_response = forms.CharField(required=False)

    class Meta:
        """Meta Class."""

        model = Entry
        # fields = ("summary", "description", "risk_types", "response",
        #           "locations", "compliances", "aro_fixed", "aro_notes")
        fields = ("summary", "description", "assumption", "locations", "evaluation_days",
                  "aro_known_multiplier", "aro_known_unit_quantity", "aro_toggle", "aro_fixed", "aro_notes",
                  "compliance_requirements", "entry_urls", "incident_response")
