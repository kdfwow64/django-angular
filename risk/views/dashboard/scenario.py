"""All views related to Impact Types in models/scenario.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    ImpactType,
    Severity,
)


@login_required
def get_all_impact_types_for_dropdown(request):
    """Get all compliances for dropdown."""
    data = []
    for impact_type in ImpactType.objects.order_by('name').all():
        data.append({'id': impact_type.id, 'name': impact_type.name})

    return JsonResponse(data, safe=False)


@login_required
def get_all_severities_for_dropdown(request):
    """Get all severity types for dropdown."""
    data = []
    for severity in Severity.objects.order_by('name').all():
        data.append({'id': severity.id, 'name': severity.name})

    return JsonResponse(data, safe=False)
