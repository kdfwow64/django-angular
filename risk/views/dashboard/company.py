"""All views related to Company in models/company.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    CompanyAsset,
    CompanyControl,
    CompanyControlMeasure,
    CompanyLocation,
)


@login_required
def get_all_company_locations_for_dropdown(request):
    """Get all company locations for dropdown."""
    data = []
    for company in CompanyLocation.objects.order_by('name').all():
        data.append({'id': company.id, 'name': company.name})

    return JsonResponse(data, safe=False)


@login_required
def get_all_company_assets_for_dropdown(request):
    """Get all company assets for dropdown."""
    data = []
    for asset in CompanyAsset.objects.order_by('name').all():
        data.append({'id': asset.id, 'name': asset.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_company_control_for_dropdown(request):
    """Get all company control for dropdown."""
    data = []
    for control in CompanyControl.objects.order_by('name').all():
        data.append({'id': control.id, 'name': control.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_company_control_measures_for_dropdown(request):
    """Get all company control measures for dropdown."""
    data = []
    for measures in CompanyControlMeasure.objects.order_by('name').all():
        data.append({'id': measures.id, 'name': measures.name})
    return JsonResponse(data, safe=False)

