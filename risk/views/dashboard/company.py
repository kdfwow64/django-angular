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
    data = {}
    # for company in CompanyLocation.objects.filter().all():
    for company in CompanyLocation.objects.filter().all():
        data.update({company.id: company.name})

    return JsonResponse(data)


@login_required
def get_all_company_assets_for_dropdown(request):
    """Get all company assets for dropdown."""
    data = {}
    # for asset in CompanyAsset.objects.filter().all():
    for asset in CompanyAsset.objects.filter().all():
        data.update({asset.id: asset.name})

    return JsonResponse(data)


@login_required
def get_all_company_control_for_dropdown(request):
    """Get all company control for dropdown."""
    data = {}
    # for control in CompanyControl.objects.filter().all():
    for control in CompanyControl.objects.filter().all():
        data.update({control.id: control.name})

    return JsonResponse(data)

@login_required
def get_all_company_control_measures_for_dropdown(request):
    """Get all company control measures for dropdown."""
    data = {}
    # for measures in CompanyControlMeasure.objects.filter().all():
    for measures in CompanyControlMeasure.objects.filter().all():
        data.update({measures.id: measures.name})

    return JsonResponse(data)

