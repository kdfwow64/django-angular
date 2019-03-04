"""All views related to Company in models/company.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    CompanyAsset,
    CompanyControl,
    CompanyControlMeasure,
    CompanyLocation,
    Company,
    Control,
    Vendor,
    ImpactCategory,
    SeverityCategory
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

@login_required
def get_company_asset(request, company_asset_id):
    """Get all compliance version with compliance id."""
    try:
        asset = CompanyAsset.objects.get(pk=int(company_asset_id))
    except:
        asset = []
    if not asset:
        data = []
    else:
        data = ({'asset_id': asset.id, 'asset_value': asset.asset_value_fixed, 'asset_percent': asset.asset_value_par, 'asset_detail': asset.description, 'asset_value_toggle': asset.asset_value_toggle})

    return JsonResponse(data, safe=False)

@login_required
def get_control_details_with_company(request, company_id):
    """Get all company control details."""
    data = []
    try:
        company_control = CompanyControl.objects.get(pk=int(company_id))
        control = Control.objects.get(pk=int(company_control.control_id))
        company = Company.objects.get(pk=int(company_control.company_id))
        vendor = Vendor.objects.get(pk=int(control.vendor_id))
        data = ({'company_name': company_control.name, 'control_name': control.name, 'vendor_name': vendor.name, 'max_loss': company.fixed_max_loss})
    except:
        pass
    return JsonResponse(data, safe=False)

@login_required
def get_all_impact_categories(request):
    """Get all Impact categories."""
    data = []
    for category in ImpactCategory.objects.order_by('name').all():
        data.append({'id': category.id, 'name': category.name, 'min': category.minimum, 'max': category.maximum})
    return JsonResponse(data, safe=False)


def get_all_severity_categories(request):
    """Get all Severity categories."""
    data = []
    for category in SeverityCategory.objects.order_by('name').all():
        data.append({'id': category.id, 'name': category.name, 'min': category.minimum, 'max': category.maximum})
    return JsonResponse(data, safe=False)