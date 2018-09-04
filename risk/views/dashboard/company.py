"""All views related to Company in models/company.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    CompanyLocation,
)


@login_required
def get_all_company_locations_for_dropdown(request):
    """Get all company locations for dropdown."""
    data = {}
    # for rt in CompanyLocation.objects.filter().all():
    for rt in CompanyLocation.objects.filter().all():
        data.update({rt.id: rt.name})

    return JsonResponse(data)

