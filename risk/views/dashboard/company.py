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
    CompanyControlLocation,
    CompanyControlSegment,
    CompanyLocation,
    CompanyAssetType,
    CompanySegment,
    Company,
    Control,
    Vendor,
    ImpactCategory,
    SeverityCategory,
    TimeUnit
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
        data = ({'asset_id': asset.id, 'asset_value': asset.get_asset_value(), 'asset_percent': asset.asset_value_par, 'asset_detail': asset.description, 'asset_value_toggle': asset.asset_value_toggle})

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
        try:
            evaluation_days = int(dat.get('evaluation_days', '0'))
        except:
            evaluation_days = 0
        try:
            type = dat.get('type')
        except:
            type = None
        try:
            owner = dat.get('owner')
        except:
            owner = None
        try:
            asset_time_unit = dat.get('asset_time_unit')
        except:
            asset_time_unit = None
        try:
            asset_value_fixed = float(dat.get('asset_value_fixed', '0'))
        except:
            asset_value_fixed = 0
        try:
            asset_quantity_fixed = float(dat.get('asset_quantity_fixed', '0'))
        except:
            asset_quantity_fixed = 0
        try:
            asset_percent = float(dat.get('asset_percent', '0'))
        except:
            asset_percent = 0
        try:
            time_unit_max = int(dat.get('time_unit_max', '0'))
        except:
            time_unit_max = 0
        try:
            time_unit_increment = float(dat.get('time_unit_increment', '0'))
        except:
            time_unit_increment = 0

        ca_id = dat.get('id')
        if ca_id is None:
            new_company_asset = CompanyAsset.objects.create(
                company_id=company.id,
                name=dat.get('name'),
                asset_type_id=type,
                description=dat.get('description'),
                asset_owner_id=owner,
                evaluation_days=evaluation_days,
                asset_value_toggle=dat.get('toggle'),
                asset_value_fixed=asset_value_fixed,
                asset_quantity_fixed=asset_quantity_fixed,
                asset_value_par=asset_percent,
                asset_timed_unit_id=asset_time_unit,
                asset_time_unit_max=time_unit_max,
                asset_time_unit_increment=time_unit_increment,
                summary_value=dat.get('summary')
            )
        else:
            new_company_asset = CompanyAsset.objects.get(pk=ca_id)
            new_company_asset.company_id = company.id
            new_company_asset.name = dat.get('name')
            new_company_asset.asset_type_id = dat.get('type')
            new_company_asset.description = dat.get('description')
            new_company_asset.asset_owner_id = dat.get('owner')
            new_company_asset.evaluation_days = evaluation_days
            new_company_asset.asset_value_toggle = dat.get('toggle')
            new_company_asset.asset_value_fixed = asset_value_fixed
            new_company_asset.asset_quantity_fixed = asset_quantity_fixed
            new_company_asset.asset_value_par = asset_percent
            new_company_asset.asset_timed_unit_id = TimeUnit.objects.get(annual_units=int(dat.get('asset_time_unit')))
            new_company_asset.asset_time_unit_max = time_unit_max
            new_company_asset.asset_time_unit_increment = time_unit_increment
            new_company_asset.summary_value = dat.get('summary')
            new_company_asset.save()

        locations = dat.get('locations', [1,])

        try:
            for cal in CompanyAssetLocation.objects.filter(id_companyasset_id=ca_id):
                try:
                    locations.remove(cal.id)
                except:
                    cal.delete()
        except:
            print(traceback.format_exc())
            pass

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


@login_required
def api_get_company_control(request, cc_id):
    """Get Company Control by id"""
    company = request.user.get_current_company()
    rv = {}
    if cc_id:
        try:
            cc = CompanyControl.objects.get(id=cc_id)
            try:
                company_locations = [loc.id_companylocation_id for loc in CompanyControlLocation.objects.filter(id_companycontrol_id=cc_id)] or [1, ]
            except:
                company_locations = None

            try:
                company_segments = [loc.id_companysegment_id for loc in CompanyControlSegment.objects.filter(id_companycontrol_id=cc_id)] or [1, ]
            except:
                company_segments = None
            try:
                vendor_select = Control.objects.get(id=cc.control_id).vendor_id
                vendor_name= Vendor.objects.get(pk=vendor_select).name
                control_select= cc.control_id
                control_name= Control.objects.get(id=cc.control_id).name
            except:
                vendor_select = None
                vendor_name = ''
                control_select = None
                control_name = ''
            rv = {
                'status': 'success',
                'code': 200,
                'new_cc': {
                    'id': cc_id,
                    'vendor_select': vendor_select,
                    'vendor_name': vendor_name,
                    'control_select': control_select,
                    'control_name': control_name,
                    'name': cc.name,
                    'alias': cc.alias,
                    'description': cc.description,
                    'version': cc.version,
                    'opex': cc.estimated_maint_opex,
                    'opex_desc': cc.opex_description,
                    'maintenance_date': cc.date_maint,
                    'recovery_multiplier': cc.recovery_multiplier,
                    'recovery_time_unit': cc.recovery_time_unit_id,
                    'company_locations': company_locations,
                    'company_segments': company_segments,
                    'evaluation_days': cc.evaluation_days,
                    'poc_main': cc.poc_main_id,
                    'poc_support': cc.poc_support_id
                }
            }
        except:
            print(traceback.format_exc())
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid control"]}
    return JsonResponse(rv)


@login_required
def api_get_company_asset(request, ca_id):
    """Get Company Asset by id"""
    company = request.user.get_current_company()
    rv = {}
    if ca_id:
        try:
            ca = CompanyAsset.objects.get(id=ca_id)
            try:
                company_locations = [loc.id_companylocation_id for loc in CompanyAssetLocation.objects.filter(id_companyasset_id=ca_id)] or [1, ]
            except:
                company_locations = None

            rv = {
                'status': 'success',
                'code': 200,
                'new_ca': {
                    'id': ca.id,
                    'name': ca.name,
                    'type': ca.asset_type_id,
                    'description': ca.description,
                    'locations': company_locations,
                    'owner': ca.asset_owner_id,
                    'evaluation_days': ca.evaluation_days,
                    'toggle': ca.asset_value_toggle,
                    'asset_value_fixed': ca.asset_value_fixed,
                    'asset_quantity_fixed': ca.asset_quantity_fixed,
                    'asset_percent': ca.asset_value_par,
                    'asset_time_unit': TimeUnit.objects.get(id=ca.asset_timed_unit_id).annual_units,
                    'time_unit_max': ca.asset_time_unit_max,
                    'time_unit_increment': ca.asset_time_unit_increment
                }
            }
        except:
            print(traceback.format_exc())
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid control"]}
    return JsonResponse(rv)


@login_required
def api_company_max_loss(request):
    """Get Company MAx Loss"""
    company = request.user.get_current_company()
    data = {
        'max_loss': company.get_company_max_loss()
    }
    return JsonResponse(data, safe=False)
