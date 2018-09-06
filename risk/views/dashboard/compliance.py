"""All views related to Compliance in models/compliance.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    Compliance,
)


@login_required
def get_all_compliances_for_dropdown(request):
    """Get all compliances for dropdown."""
    data = []
    for compliance in Compliance.objects.order_by('name').all():
        data.append({'id': compliance.id, 'name': compliance.name})

    return JsonResponse(data, safe=False)

