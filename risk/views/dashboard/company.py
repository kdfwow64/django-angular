"""All views related to Company in models/company.py."""
import json
import traceback
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    CompanyAsset,
    CompanyAssetLocation,
    CompanyControl,
    CompanyControlMeasure,
    CompanyLocation,
    CompanyAssetType,
    CompanySegment,
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
    company_id = request.user.get_current_company().id
    for asset in CompanyAsset.objects.filter(company_id=company_id):
        data.append({'id': asset.id, 'name': asset.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_company_control_for_dropdown(request):
    """Get all company control for dropdown."""
    data = []
    company_id = request.user.get_current_company().id
    for control in CompanyControl.objects.filter(company_id=company_id):
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


@login_required
def get_all_severity_categories(request):
    """Get all Severity categories."""
    data = []
    for category in SeverityCategory.objects.order_by('name').all():
        data.append({'id': category.id, 'name': category.name, 'min': category.minimum, 'max': category.maximum})
    return JsonResponse(data, safe=False)

@login_required
def get_all_company_segments_for_dropdown(request):
    """Get all company segments for dropdown."""
    data = []
    for segment in CompanySegment.objects.order_by('name').all():
        data.append({'id': segment.id, 'name': segment.name})

    return JsonResponse(data, safe=False)

@login_required
def get_all_company_asset_type(request):
    """Get all company asset type for dropdown."""
    company_id = request.user.get_current_company().id
    data = []
    # for type in CompanyAssetType.objects.filter(company_id=company_id):
    for type in CompanyAssetType.objects.order_by('name').all():
        data.append({'id': type.id, 'name': type.name})
    return JsonResponse(data, safe=False)

@login_required
def get_company_annual_revenue(request):
    """Get company annual revenue"""
    company = request.user.get_current_company()
    data = {'id': company.id, 'name': company.name, 'annual_revenue': company.annual_revenue}
    return JsonResponse(data, safe=False)

@login_required
def api_save_company_asset(request):
    """Save New Company Asset"""
    company = request.user.get_current_company()
    dat = json.loads(request.body.decode('utf-8'))
    try:
        evaluation_days = int(dat.get('evaluation_days', '0'))
        asset_value_fixed = float(dat.get('asset_value_fixed', '0'))
        asset_quantity_fixed = float(dat.get('asset_quantity_fixed', '0'))
        asset_percent = float(dat.get('asset_percent', '0'))
        time_unit_max = int(dat.get('time_unit_max', '0'))
        time_unit_increment = float(dat.get('time_unit_increment', '0'))

        new_company_asset = CompanyAsset.objects.create(
            company_id=company.id,
            name=dat.get('name'),
            asset_type_id=dat.get('type'),
            description=dat.get('description'),
            asset_owner_id=dat.get('owner'),
            evaluation_days=evaluation_days,
            asset_value_toggle=dat.get('toggle'),
            asset_value_fixed=asset_value_fixed,
            asset_quantity_fixed=asset_quantity_fixed,
            asset_value_par=asset_percent,
            asset_timed_unit_id=dat.get('asset_time_unit'),
            asset_time_unit_max=time_unit_max,
            asset_time_unit_increment=time_unit_increment,
            summary_value=dat.get('summary')
        )

        locations = dat.get('locations', [1,])
        try:
            for loc in locations:
                try:
                    CompanyAssetLocation.objects.create(
                        id_companyasset_id=new_company_asset.id,
                        id_companylocation_id=loc
                    )
                except:
                    pass
        except:
            pass

        rv = {
            'status': 'success',
            'code': 200,
            'new_company_asset': {
                'id': new_company_asset.id,
                'name': new_company_asset.name
            }
        }
    except:
        print(traceback.format_exc())
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid control"]}
    return JsonResponse(rv)