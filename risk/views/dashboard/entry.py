"""All views related to Entry in models/entry.py."""
import json
import os
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import traceback

from django.http import JsonResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.forms import URLField
from django.views import View
from decimal import *
from risk.models import (
    Actor,
    ActorIntent,
    ActorMotive,
    CompanyControl,
    CompanyContact,
    CompanyControlLocation,
    CompanyControlSegment,
    CompanyControlMeasure,
    CompanyLocation,
    CompanyAssetType,
    CompanyAssetLocation,
    # CompanyAssetSegment,
    Compliance,
    Entry,
    EntryActor,
    EntryActorIntent,
    EntryActorMotive,
    EntryCompanyAsset,
    EntryCompanyControl,
    EntryCompanyControlMeasure,
    EntryCompanyLocation,
    Response,
    RiskType,
    TimeUnit,
    FrequencyCategory,
    EntryUrl,
    ComplianceType,
    ComplianceRequirement,
    EntryCompliance,
    EntryComplianceRequirement,
    CompanyAsset,
    SeverityCategory,
    Company,
    CompanyArtifact,
    EntryCompanyArtifact,
    EntryAncillaryType,
    EntryAncillary,
    Vendor,
    Control,
    ControlCategory,
    ControlCategoryControl,
    ImpactCategory
)
from risk.forms.entry import(
    RiskEntryBasicForm,
)
from django.conf import settings
from django.http import HttpResponse, Http404


def __init__(self, location=None, base_url=None, file_permissions_mode=None,
             directory_permissions_mode=None):
    self.file_permissions_mode = (
        file_permissions_mode if file_permissions_mode is not None
        else settings.FILE_UPLOAD_PERMISSIONS
    )
    self.directory_permissions_mode = (
        directory_permissions_mode if directory_permissions_mode is not None
        else settings.FILE_UPLOAD_DIRECTORY_PERMISSIONS
    )

# @login_required
# def file_download(request):
#     path = request.body.decode('utf-8')
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404


@login_required
def file_upload(request, count, entry_id, company_id):
    try:
        for each in EntryCompanyArtifact.objects.order_by('id').all():
            deleted_items = request.POST['deleted_items']
            try:
                temp = 'Del' + str(each.id) + 'Item'
                if temp in deleted_items:
                    file = CompanyArtifact.objects.get(
                        pk=each.id_companyartifact_id)
                    try:
                        file.artifact_file.delete()
                    except:
                        pass
                    file.delete()
                    each.delete()
            except:
                pass
    except:
        pass
    if request.method == 'POST' and request.FILES:
        st = 'file_'
        for i in range(0, int(count)):
            item = st + str(i)
            try:
                file = request.FILES[item]
                name = request.POST[item + '_name']
                desc = request.POST[item + '_desc']
                artifact = CompanyArtifact.objects.get_or_create(
                    artifact_file=file, name=name, description=desc, company_id=int(company_id))
                EntryCompanyArtifact.objects.get_or_create(id_companyartifact_id=artifact[
                                                           0].id, id_entry_id=int(entry_id))
            except:
                pass
    return JsonResponse({'data': 'success'})


@login_required
def api_list_risk_entries(request):
    """List entries."""
    user = request.user
    try:
        company = user.get_current_company()
        # Get fist register for company from entry.py/Register
        company_register = company.get_active_register()

        rows = []
        total = 0

        register_entries = company_register.entry
        total = register_entries.count()
        rate_relation = {}
        for entry in register_entries.order_by('-date_modified').all():
            if entry.aro_toggle == 'C':
                frequency_category = FrequencyCategory.objects.get(
                    id=entry.aro_frequency_id)
                rate_relation = {
                    'minimum': frequency_category.minimum,
                    'maximum': frequency_category.maximum
                }
            elif entry.aro_toggle == 'K':
                pass
            else:
                time_unit = TimeUnit.objects.get(
                    id=entry.aro_time_unit_id)
                rate_relation = {
                    'annual_units': time_unit.annual_units
                }

            category_name = ''
            try:
                for category in SeverityCategory.objects.order_by('name').all():
                    if float(entry.residual_ale_rate / 100) >= category.minimum and float(entry.residual_ale_rate / 100) < category.maximum:
                        category_name = category.name  # changed
                if int(entry.residual_ale_rate / 100) >= 1:  # changed
                    category_name = 'Critical'
            except:
                pass
            rows.append({
                'owner_name': entry.entry_owner.full_name,
                'compliance': entry.has_compliance,
                'completed': entry.has_completed(rate_relation),
                'entry_number': entry.id,  # Entry number
                'response': entry.response_name,
                'mr': entry.mitigation_rate,  #
                'residual_ale_category': category_name,  #
                # changed
                'residual_ale_rate': str(round(entry.get_residual_ale_rate() / Decimal(company.get_company_max_loss()) * 100, 3)) + '%',
                'summary': entry.get_summary(),
                'evaluated': entry.date_evaluated.strftime("%m/%d/%Y") if entry.date_evaluated else '',
                'modified_date': entry.date_modified.strftime("%m/%d/%Y"),
                'response_plan': 'Yes' if entry.incident_response else 'No',
                'id': entry.id
            })

        data = {
            'data': rows,
            'draw': int(request.GET.get('draw', 0)),
            'recordsTotal': total,
            'recordsFiltered': len(rows),
        }
    except:
        print(traceback.format_exc())
        data = {

        }
    return JsonResponse(data)


@login_required
def api_list_vendors(request):
    """List Vendors."""
    company = request.user.get_current_company()
    try:
        rows = []
        total = 0
        for vendor in Vendor.objects.filter(company_id__in=[1, company.id]):
            parent_name = ''
            if vendor.parent_id is not None:
                try:
                    parent_name = Vendor.objects.get(id=vendor.parent_id).name
                except:
                    parent_name = ''

            url_form_field = URLField()
            try:
                url = url_form_field.clean(vendor.url_main)
                url_validation = 1
            except:
                url_validation = 0


            rows.append({
                'id': vendor.id,
                'name': vendor.name,
                'abbrv': vendor.abbrv,
                'aka': vendor.name_aka,
                'url': vendor.url_main,
                'parent': parent_name,
                'description': vendor.description,
                'keywords': vendor.keywords,
                'url_validation': url_validation
            })
            total +=1

        data = {
            'data': rows,
            'draw': int(request.GET.get('draw', 0)),
            'recordsTotal': total,
            'recordsFiltered': len(rows),
        }
    except:
        print(traceback.format_exc())
        data = {

        }
    return JsonResponse(data)

@login_required
def api_company_control_list(request):
    """Company Control List."""
    company = request.user.get_current_company()
    user = request.user
    try:
        rows = []
        total = 0
        for cc in CompanyControl.objects.filter(company_id__in=[1, company.id]):
            vendor_name = ''
            vendor_abbrv = ''
            vendor_aka = ''
            try:
                control_ob = Control.objects.get(id=cc.control_id)
                control_name = control_ob.name
                control_abbrv = control_ob.abbrv
                control_description = control_ob.description
                try:
                    vendor_ob = Vendor.objects.get(id=control_ob.vendor_id)
                    vendor_name = vendor_ob.name
                    vendor_abbrv = vendor_ob.abbrv
                    vendor_aka = vendor_ob.name_aka
                except:
                    pass
            except:
                control_name = ''
                control_description = ''
                control_abbrv = ''

            try:
                company_contact = CompanyContact.objects.get(id=cc.poc_main_id)
                poc_main = company_contact.first_name + company_contact.last_name
            except:
                poc_main = ''

            protection_mitigated_ale_cost_sum = 0
            protection_inherent_ale_cost_sum = 0

            try:
                for e_cc in EntryCompanyControl.objects.filter(id_companycontrol_id=cc.id):
                    entry = Entry.objects.get(id=e_cc.id_entry_id)

                    aro_rate = 0
                    rate_relation = {}
                    if entry.aro_toggle == 'C':
                        frequency_category = FrequencyCategory.objects.get(
                            id=entry.aro_frequency_id)
                        rate_relation = {
                            'minimum': frequency_category.minimum,
                            'maximum': frequency_category.maximum
                        }
                        aro_rate = (frequency_category.minimum +
                                    frequency_category.maximum) / 2 * 100
                        if frequency_category.minimum == 1:
                            aro_rate = 100
                    elif entry.aro_toggle == 'K':
                        aro_rate = entry.aro_fixed
                    else:
                        time_unit = TimeUnit.objects.get(
                            id=entry.aro_time_unit_id)
                        rate_relation = {
                            'annual_units': time_unit.annual_units
                        }
                        aro_rate = entry.aro_known_multiplier * \
                                   time_unit.annual_units / entry.aro_known_unit_quantity
                        if aro_rate >= 1:
                            aro_rate = 100
                        else:
                            aro_rate *= 100
                    aro_rate = entry.get_aro_rate()
                    aro_rate = Decimal(aro_rate)
                    if entry.is_qualified(rate_relation):
                        # Total SLE
                        total_sle = 0
                        total_ale = 0
                        try:
                            total_asset_value = 0
                            for entry_company_asset in entry.companyasset_entry.order_by('id').all():
                                company_asset = CompanyAsset.objects.get(
                                    pk=entry_company_asset.id_companyasset_id)
                                sle_value = round(
                                    Decimal(company_asset.get_asset_value()) *
                                    Decimal(entry_company_asset.exposure_factor_rate) / 100,
                                    2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                                    entry_company_asset.exposure_factor_fixed, 2)
                                ale_value = round(Decimal(company_asset.get_asset_value()) * Decimal(
                                    entry_company_asset.exposure_factor_rate) * aro_rate / 10000,
                                                  2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                                    Decimal(entry_company_asset.exposure_factor_fixed) * aro_rate / 100, 2)
                                total_asset_value += round(
                                    company_asset.get_asset_value(), 2)
                                total_sle += sle_value
                                total_ale += ale_value

                            for ancillary in entry.entryentryancillary.order_by('id').all():
                                try:
                                    total_sle += ancillary.per_occurance * ancillary.ancillary_fixed
                                except:
                                    pass

                                try:
                                    total_ale += ancillary.per_occurance * ancillary.ancillary_fixed * aro_rate / 100
                                except:
                                    pass
                        except:
                            pass
                        # Mitigating Info
                        total_ale_impact = 0
                        try:
                            total_sle_rate = 0
                            for mitigating_control in entry.companycontrol_entry.order_by('id').all():
                                total_sle_rate += mitigating_control.sle_mitigation_rate
                            total_sle_rate = Decimal(total_sle_rate)
                            total_aro_rate = 0
                            total_sle_cost = 0
                            total_aro_cost = 0
                            total_cost = 0
                            for mitigating_control in entry.companycontrol_entry.order_by('id').all():
                                if mitigating_control.id_companycontrol_id == cc.id:
                                    company_control = CompanyControl.objects.get(
                                        pk=mitigating_control.id_companycontrol_id)
                                    company = Company.objects.get(
                                        pk=company_control.company_id)
                                    control = Control.objects.get(
                                        pk=company_control.control_id)
                                    vendor = Vendor.objects.get(pk=control.vendor_id)
                                    sle_cost_value = round(
                                        total_sle * Decimal(mitigating_control.sle_mitigation_rate) / 100, 2)
                                    aro_cost_value = round(
                                        total_sle * (100 - total_sle_rate) * Decimal(
                                            mitigating_control.aro_mitigation_rate) / 10000, 2)
                                    total_cost_value = sle_cost_value + aro_cost_value
                                    impact_value = round(total_cost_value * aro_rate / 100, 2)
                                    total_sle_cost += sle_cost_value
                                    total_aro_cost += aro_cost_value
                                    total_cost += total_cost_value
                                    total_ale_impact += impact_value
                                    total_aro_rate += mitigating_control.aro_mitigation_rate
                        except:
                            pass
                        # protection_inherent_ale_cost_sum += total_ale if entry.response_name == 'Treat' else 0
                        # protection_residual_ale_cost_sum += Decimal(
                        #     total_ale - total_ale_impact) if entry.response_name == 'Treat' else 0
                        protection_mitigated_ale_cost_sum += total_ale_impact
                        protection_inherent_ale_cost_sum += total_ale
                    else:
                        pass
            except:
                pass


            try:
                ttr = str(int(cc.recovery_multiplier)) + ' ' + cc.recovery_time_unit.name
            except:
                ttr = ''

            try:
                annual_cost = cc.estimated_maint_opex + cc.estimated_dependency_opex
            except:
                annual_cost = 0;
            rows.append({
                'id': cc.id,
                'cc_name': cc.name,
                'control_name': control_name,
                'cc_poc_main': poc_main,
                'annual_mitigation': '$' + '{:,}'.format(protection_mitigated_ale_cost_sum),
                'annual_cost': '$' + '{:,}'.format(annual_cost),
                'ttr': ttr,
                'abbrv': cc.abbrv,
                'alias': cc.alias,
                'description': cc.description,
                'control_abbrv': control_abbrv,
                'control_description': control_description,
                'vendor_name': vendor_name,
                'vendor_abbrv': vendor_abbrv,
                'vendor_aka': vendor_aka
            })
            total += 1

        data = {
            'data': rows,
            'draw': int(request.GET.get('draw', 0)),
            'recordsTotal': total,
            'recordsFiltered': len(rows),
        }
    except:
        data = {

        }
    return JsonResponse(data)



@login_required
def api_get_company_control_detail(request, cc_id):
    """Get Company Control by id"""
    company = request.user.get_current_company()
    rows = []
    total = 0
    data = {}
    if cc_id:
        try:
            for e_cc in EntryCompanyControl.objects.filter(id_companycontrol_id=cc_id):
                entry = Entry.objects.get(id=e_cc.id_entry_id)
                aro_rate = 0
                rate_relation = {}
                if entry.aro_toggle == 'C':
                    frequency_category = FrequencyCategory.objects.get(
                        id=entry.aro_frequency_id)
                    rate_relation = {
                        'minimum': frequency_category.minimum,
                        'maximum': frequency_category.maximum
                    }
                    aro_rate = (frequency_category.minimum +
                                frequency_category.maximum) / 2 * 100
                    if frequency_category.minimum == 1:
                        aro_rate = 100
                elif entry.aro_toggle == 'K':
                    aro_rate = entry.aro_fixed
                else:
                    time_unit = TimeUnit.objects.get(
                        id=entry.aro_time_unit_id)
                    rate_relation = {
                        'annual_units': time_unit.annual_units
                    }
                    aro_rate = entry.aro_known_multiplier * \
                               time_unit.annual_units / entry.aro_known_unit_quantity
                    if aro_rate >= 1:
                        aro_rate = 100
                    else:
                        aro_rate *= 100
                aro_rate = entry.get_aro_rate()
                aro_rate = Decimal(aro_rate)
                if entry.is_qualified(rate_relation):
                    total_sle = 0
                    total_ale = 0
                    try:
                        total_asset_value = 0
                        for entry_company_asset in entry.companyasset_entry.order_by('id').all():
                            company_asset = CompanyAsset.objects.get(
                                pk=entry_company_asset.id_companyasset_id)
                            sle_value = round(
                                Decimal(company_asset.get_asset_value()) *
                                Decimal(entry_company_asset.exposure_factor_rate) / 100,
                                2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                                entry_company_asset.exposure_factor_fixed, 2)
                            ale_value = round(Decimal(company_asset.get_asset_value()) * Decimal(
                                entry_company_asset.exposure_factor_rate) * aro_rate / 10000,
                                              2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                                Decimal(entry_company_asset.exposure_factor_fixed) * aro_rate / 100, 2)
                            total_asset_value += round(
                                company_asset.get_asset_value(), 2)
                            total_sle += sle_value
                            total_ale += ale_value

                        for ancillary in entry.entryentryancillary.order_by('id').all():
                            try:
                                total_sle += ancillary.per_occurance * ancillary.ancillary_fixed
                            except:
                                pass

                            try:
                                total_ale += ancillary.per_occurance * ancillary.ancillary_fixed * aro_rate / 100
                            except:
                                pass
                    except:
                        pass
                    # Mitigating Info

                    total_aro_rate = 0
                    total_sle_cost = 0
                    total_aro_cost = 0
                    total_cost = 0
                    total_ale_impact = 0
                    try:
                        total_sle_rate = 0
                        for mitigating_control in entry.companycontrol_entry.order_by('id').all():
                            total_sle_rate += mitigating_control.sle_mitigation_rate
                        total_sle_rate = Decimal(total_sle_rate)
                        for mitigating_control in entry.companycontrol_entry.order_by('id').all():
                            if mitigating_control.id_companycontrol_id == int(cc_id):
                                company_control = CompanyControl.objects.get(
                                    pk=mitigating_control.id_companycontrol_id)
                                company = Company.objects.get(
                                    pk=company_control.company_id)
                                control = Control.objects.get(
                                    pk=company_control.control_id)
                                vendor = Vendor.objects.get(pk=control.vendor_id)
                                sle_cost_value = round(
                                    total_sle * Decimal(mitigating_control.sle_mitigation_rate) / 100, 2)
                                aro_cost_value = round(
                                    total_sle * (100 - total_sle_rate) * Decimal(
                                        mitigating_control.aro_mitigation_rate) / 10000, 2)
                                total_cost_value = sle_cost_value + aro_cost_value
                                impact_value = round(total_cost_value * aro_rate / 100, 2)
                                total_sle_cost += sle_cost_value
                                total_aro_cost += aro_cost_value
                                total_cost += total_cost_value
                                total_ale_impact += impact_value
                                total_aro_rate += mitigating_control.aro_mitigation_rate
                    except:
                        pass

                    rows.append({
                        'id': entry.id,
                        'summary': entry.summary,
                        'sle_cost': '($' + '{:,}'.format(total_sle_cost) + ')',
                        'aro_cost': '($' + '{:,}'.format(total_aro_cost) + ')',
                        'ale_mitigation': '($' + '{:,}'.format(total_ale_impact) + ')',
                        'compliance_entry': 'Yes' if EntryCompliance.objects.filter(id_entry_id=entry.id).count() > 0 else 'No'
                    })
                    total += 1
                else:
                    pass

            data = {
                'data': rows,
                'draw': int(request.GET.get('draw', 0)),
                'recordsTotal': total,
                'recordsFiltered': len(rows),
            }
        except:
            print(traceback.format_exc())
            data = {}

    return JsonResponse(data)

@login_required
def api_get_company_asset_detail(request, ca_id):
    """Company Asset Detail."""
    company = request.user.get_current_company()
    user = request.user
    rows = []
    total = 0
    data = {}
    if ca_id:
        try:
            for e_ca in EntryCompanyAsset.objects.filter(id_companyasset_id=ca_id):
                entry = Entry.objects.get(id=e_ca.id_entry_id)
                aro_rate = 0
                rate_relation = {}
                if entry.aro_toggle == 'C':
                    frequency_category = FrequencyCategory.objects.get(
                        id=entry.aro_frequency_id)
                    rate_relation = {
                        'minimum': frequency_category.minimum,
                        'maximum': frequency_category.maximum
                    }
                    aro_rate = (frequency_category.minimum +
                                frequency_category.maximum) / 2 * 100
                    if frequency_category.minimum == 1:
                        aro_rate = 100
                elif entry.aro_toggle == 'K':
                    aro_rate = entry.aro_fixed
                else:
                    time_unit = TimeUnit.objects.get(
                        id=entry.aro_time_unit_id)
                    rate_relation = {
                        'annual_units': time_unit.annual_units
                    }
                    aro_rate = entry.aro_known_multiplier * \
                               time_unit.annual_units / entry.aro_known_unit_quantity
                    if aro_rate >= 1:
                        aro_rate = 100
                    else:
                        aro_rate *= 100

                aro_rate = entry.get_aro_rate()
                aro_rate = Decimal(aro_rate)
                if entry.is_qualified(rate_relation):
                    # Total SLE
                    total_sle = 0
                    total_ale = 0
                    try:
                        total_asset_value = 0
                        for entry_company_asset in entry.companyasset_entry.order_by('id').all():
                            if entry_company_asset.id_companyasset_id == int(ca_id):
                                company_asset = CompanyAsset.objects.get(
                                    pk=entry_company_asset.id_companyasset_id)
                                sle_value = round(
                                    Decimal(company_asset.get_asset_value()) *
                                    Decimal(entry_company_asset.exposure_factor_rate) / 100,
                                    2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                                    entry_company_asset.exposure_factor_fixed, 2)
                                ale_value = round(Decimal(company_asset.get_asset_value()) * Decimal(
                                    entry_company_asset.exposure_factor_rate) * aro_rate / 10000,
                                                  2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                                    Decimal(entry_company_asset.exposure_factor_fixed) * aro_rate / 100, 2)
                                total_asset_value += round(
                                    company_asset.get_asset_value(), 2)
                                total_sle += sle_value
                                total_ale += ale_value
                    except:
                        pass

                    rows.append({
                        'id': entry.id,
                        'summary': entry.summary,
                        'aro_toggle': 'Frequency' if entry.aro_toggle == 'C' else 'Percent' if entry.aro_toggle == 'K' else 'Time Based',
                        'sle_cost': '$' + '{:,}'.format(total_sle),
                        'ale_cost': '$' + '{:,}'.format(total_ale)
                    })
                    total += 1
                else:
                    pass
            data = {
                'data': rows,
                'draw': int(request.GET.get('draw', 0)),
                'recordsTotal': total,
                'recordsFiltered': len(rows),
            }
        except:
            print(traceback.format_exc())
            data = {}
    return JsonResponse(data)



@login_required
def api_company_asset_list(request):
    """Company Asset List."""
    company = request.user.get_current_company()
    user = request.user
    try:
        rows = []
        total = 0
        for asset in CompanyAsset.objects.filter(company_id=company.id):
            total_ale_sum = 0
            try:
                for e_ca in EntryCompanyAsset.objects.filter(id_companyasset_id=asset.id):
                    entry = Entry.objects.get(id=e_ca.id_entry_id)
                    aro_rate = 0
                    rate_relation = {}
                    if entry.aro_toggle == 'C':
                        frequency_category = FrequencyCategory.objects.get(
                            id=entry.aro_frequency_id)
                        rate_relation = {
                            'minimum': frequency_category.minimum,
                            'maximum': frequency_category.maximum
                        }
                        aro_rate = (frequency_category.minimum +
                                    frequency_category.maximum) / 2 * 100
                        if frequency_category.minimum == 1:
                            aro_rate = 100
                    elif entry.aro_toggle == 'K':
                        aro_rate = entry.aro_fixed
                    else:
                        time_unit = TimeUnit.objects.get(
                            id=entry.aro_time_unit_id)
                        rate_relation = {
                            'annual_units': time_unit.annual_units
                        }
                        aro_rate = entry.aro_known_multiplier * \
                                   time_unit.annual_units / entry.aro_known_unit_quantity
                        if aro_rate >= 1:
                            aro_rate = 100
                        else:
                            aro_rate *= 100

                    aro_rate = entry.get_aro_rate()
                    aro_rate = Decimal(aro_rate)
                    if entry.is_qualified(rate_relation):
                        # Total SLE
                        total_sle = 0
                        total_ale = 0
                        try:
                            total_asset_value = 0
                            for entry_company_asset in entry.companyasset_entry.order_by('id').all():
                                if entry_company_asset.id_companyasset_id == asset.id:
                                    company_asset = CompanyAsset.objects.get(
                                        pk=entry_company_asset.id_companyasset_id)
                                    sle_value = round(
                                        Decimal(company_asset.get_asset_value()) *
                                        Decimal(entry_company_asset.exposure_factor_rate) / 100,
                                        2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                                        entry_company_asset.exposure_factor_fixed, 2)
                                    ale_value = round(Decimal(company_asset.get_asset_value()) * Decimal(
                                        entry_company_asset.exposure_factor_rate) * aro_rate / 10000,
                                                      2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                                        Decimal(entry_company_asset.exposure_factor_fixed) * aro_rate / 100, 2)
                                    total_asset_value += round(
                                        company_asset.get_asset_value(), 2)
                                    total_sle += sle_value
                                    total_ale += ale_value

                        except:
                            pass
                        total_ale_sum += total_ale
                    else:
                        pass
            except:
                pass

            try:
                asset_type = CompanyAssetType.objects.get(id=asset.asset_type_id).name
            except:
                asset_type = ''

            try:
                owner = CompanyContact.objects.get(id=asset.asset_owner_id)
                asset_owner = owner.first_name + owner.last_name
            except:
                asset_owner = ''
            rows.append({
                'id': asset.id,
                'name': asset.name,
                'type': asset_type,
                'owner': asset_owner,
                'toggle': asset.asset_value_toggle,
                'asset_value': '$' + '{:,}'.format(round(asset.get_asset_value(), 2)),  # str(round(asset.get_asset_value(), 2))
                'annual_exposure': '$' + '{:,}'.format(round(total_ale_sum, 2))
            })
            total += 1

        data = {
            'data': rows,
            'draw': int(request.GET.get('draw', 0)),
            'recordsTotal': total,
            'recordsFiltered': len(rows),
        }
    except:
        print(traceback.format_exc())
        data = {
        }
    return JsonResponse(data)


@login_required
def api_list_controls(request, vendor_id):
    """List Controls."""
    company_id = request.user.get_current_company().id
    try:
        rows = []
        total = 0
        for control in Control.objects.filter(company_id__in=[1, company_id], vendor_id=vendor_id):
            try:
                controlcategory = ''
                for cc in ControlCategoryControl.objects.filter(id_control_id=control.id):
                    controlcategory = controlcategory + ControlCategory.objects.get(id=cc.id_controlcategory_id).name + '\n'

                rows.append({
                    'id': control.id,
                    'name': control.name,
                    'category': controlcategory,
                    'aka': control.name_aka,
                    'url': control.url,
                    'abbrv': control.abbrv,
                    'description': control.description
                })
                total += 1
            except:
                data = {

                }

        data = {
            'data': rows,
            'draw': int(request.GET.get('draw', 0)),
            'recordsTotal': total,
            'recordsFiltered': len(rows),
        }
    except:
        data = {

        }
    return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class FileUploadView(View):
    # parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):

        file_obj = request.data['file']
        str = ''
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)


@method_decorator(login_required, name='dispatch')
class CreateRiskEntry(View):
    """Create Risk Entry."""

    form_class = RiskEntryBasicForm

    def post(self, request, *args, **kwargs):
        """Handle post requests."""
        request_data = json.loads(request.body.decode('utf-8'))
        user = request.user
        company = user.get_current_company()
        # return JsonResponse({})
        entry_id = request_data.get('entry_id')
        if entry_id is None:
            form = self.form_class(data=request_data)
        else:
            risk_entry = Entry.objects.get(pk=entry_id)
            form = self.form_class(instance=risk_entry, data=request_data)

        if form.is_valid():
            risk_entry = form.save(commit=False)
            if entry_id is None:
                risk_entry.register = request.user.get_current_company().get_active_register()
                risk_entry.created_by = request.user
            risk_entry.response_id = int(
                request_data.get("response", request.user.id))
            risk_entry.entry_owner_id = int(
                request_data.get("entry_owner", request.user.id))
            risk_entry.aro_toggle = request_data.get(
                "aro_toggle", request.user.id)
            risk_entry.aro_known_multiplier = request_data.get(
                "aro_known_multiplier", request.user.id)
            risk_entry.aro_known_unit_quantity = request_data.get(
                "aro_known_unit_quantity", request.user.id)
            risk_entry.aro_time_unit_id = request_data.get(
                "aro_time_unit", request.user.id)
            risk_entry.aro_fixed = request_data.get(
                "aro_fixed", request.user.id)
            risk_entry.aro_frequency_id = request_data.get(
                "aro_frequency", request.user.id)
            risk_entry.modified_by = request.user
            risk_entry.save()

            # Select multiple dropdowns - Company locations
            selected_cl = request_data.get(
                "locations", [1, ])  # 1 - All company locations
            for ecl in risk_entry.entry_companylocation.all():
                try:
                    selected_cl.remove(ecl.id_companylocation_id)
                except:  # This company location is not selected anymore
                    ecl.delete()
            # Add new Company Locations
            for location_id in selected_cl:  # 1 - All company locations
                try:
                    location = CompanyLocation.objects.get(pk=location_id)
                    EntryCompanyLocation.objects.get_or_create(
                        id_entry=risk_entry, id_companylocation=location)
                except:
                    pass

            for ecp in risk_entry.entrycompliancerequirement.all():
                try:
                    ecp.delete()
                except:  # This Compliance is not selected anymore
                    pass

            selected_compliance_requirements = request_data.get(
                "compliance_requirements", [])

            for requirement in selected_compliance_requirements:
                try:
                    requirement_item = ComplianceRequirement.objects.get(
                        pk=requirement['requirement_id'])
                    EntryComplianceRequirement.objects.get_or_create(
                        id_entry=risk_entry, id_compliance_requirement=requirement_item)
                except:
                    pass
            # Entry Url
            for eurl in EntryUrl.objects.filter(entry_id=risk_entry.id):
                try:
                    eurl.delete()
                except:  # This Compliance is not selected anymore
                    pass
            entry_urls = request_data.get("entry_urls", [])
            for entry_url in entry_urls:
                try:
                    EntryUrl.objects.get_or_create(
                        entry=risk_entry, url=entry_url['url'], description=entry_url['desc'], name=entry_url['name'], is_internal=entry_url['type'])
                except:
                    pass
            rv = {'status': 'success', 'code': 200, 'id': risk_entry.id, 'company_id': company.id, 'created_date': risk_entry.date_created.strftime(
                "%m/%d/%Y"), 'modified_date': risk_entry.date_modified.strftime("%m/%d/%Y"), 'evaluated_date': risk_entry.date_evaluated.strftime("%m/%d/%Y") if risk_entry.date_evaluated else ''}
        else:
            rv = {'status': 'error', 'code': 400, 'errors': form.errors}

        return JsonResponse(rv)


@login_required
def api_update_threat_details(request, entry_id):
    """Update threat entry."""
    try:
        if request.method == 'POST':
            risk_entry = Entry.objects.get(pk=entry_id)
            payload = json.loads(request.body.decode(
                'utf-8')).get("multidata", [])
            try:
                for item in EntryActor.objects.filter(id_entry_id=entry_id):
                    try:
                        for i_item in EntryActorIntent.objects.filter(id_entryactor_id=item.id):
                            try:
                                i_item.delete()
                            except:
                                pass
                        for m_item in EntryActorMotive.objects.filter(id_entryactor_id=item.id):
                            try:
                                m_item.delete()
                            except:
                                pass
                        item.delete()
                    except:
                        pass
            except:
                pass
            for request_data in payload:
                try:
                    actor = Actor.objects.get(
                        pk=request_data.get('actor_name_id'))

                    entry_actor = EntryActor.objects.create(
                        id_entry=risk_entry, id_actor=actor, detail=request_data.get('detail'))

                    # Select multiple dropdowns - Intensions
                    selected_intents = request_data.get("intentions_id", [])

                    for intention_id in selected_intents:
                        try:
                            intention = ActorIntent.objects.get(
                                pk=intention_id)
                            EntryActorIntent.objects.create(
                                id_entryactor=entry_actor, id_actorintent=intention)
                        except:
                            pass

                    # Select multiple dropdowns - Motives
                    selected_motives = request_data.get("motives_id", [])

                    for motives_id in selected_motives:
                        try:
                            motive = ActorMotive.objects.get(pk=motives_id)
                            EntryActorMotive.objects.create(
                                id_entryactor=entry_actor, id_actormotive=motive)
                        except:
                            pass
                except:
                    rv = {'status': 'error', 'code': 400,
                          'errors': ["Invalid actor"]}

            rv = {'status': 'success', 'code': 200, 'id': risk_entry.id}
        else:
            rv = {'status': 'error', 'code': 400,
                  'errors': ["Invalid HTTP method"]}
    except:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid risk entry"]}

    return JsonResponse(rv)


@login_required
def api_update_affected_assets(request, entry_id):
    """Update threat entry."""
    try:
        if request.method == 'POST':
            risk_entry = Entry.objects.get(pk=entry_id)
            data = json.loads(request.body.decode('utf-8'))
            payload = data.get("multidata", [])
            try:
                for del_item in EntryCompanyAsset.objects.filter(id_entry_id=risk_entry.id):
                    del_item.delete()

                for request_data in payload:
                    # Get current company asset (if any)
                    try:
                        asset = CompanyAsset.objects.get(
                            pk=int(request_data.get('name_id')))
                        toggle = request_data.get('exposure_factor_toggle')
                        entry_asset_id = request_data.get('entry_asset_id')
                        EntryCompanyAsset.objects.create(
                            id_entry=risk_entry,
                            id_companyasset=asset,
                            detail=request_data.get('detail'),
                            exposure_factor_toggle=toggle,
                            exposure_factor_fixed=0 if toggle == 'P' else request_data.get(
                                'exposure_factor_fixed'),
                            exposure_factor_rate=0 if toggle == 'F' else request_data.get(
                                'exposure_factor_rate')
                        )
                    except:
                        rv = {'status': 'error', 'code': 400,
                              'errors': ["Invalid asset"]}
            except:
                pass
            ancillary_items = data.get("ancillary_items", [])
            for del_item in EntryAncillary.objects.filter(entry_id=risk_entry.id):
                del_item.delete()

            for request_data in ancillary_items['multidata']:
                # Get current company asset (if any)
                try:
                    EntryAncillary.objects.create(
                        entry_id=risk_entry.id,
                        ancillary_type_id=request_data.get('type_id'),
                        summary=request_data.get('summary'),
                        description=request_data.get('description'),
                        ancillary_fixed=request_data.get('cost'),
                        cost_detail=request_data.get('detail'),
                        per_occurance=request_data.get('occurences'),
                        evaluation_days=request_data.get('evaluation_days')
                    )
                except:
                    print(traceback.format_exc())
                    rv = {'status': 'error', 'code': 400,
                          'errors': ["Invalid asset"]}

            rv = {'status': 'success', 'code': 200, 'id': risk_entry.id}
        else:
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}
    except:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}

    return JsonResponse(rv)


@login_required
def api_update_mitigating_controls(request, entry_id):
    """Update threat entry."""
    try:
        if request.method == 'POST':
            risk_entry = Entry.objects.get(pk=entry_id)
            data = json.loads(request.body.decode('utf-8'))
            payload = data.get("multidata", [])
            residual_ale_rate = data.get('residual_ale_rate')
            risk_entry.residual_ale_rate = residual_ale_rate
            risk_entry.mitigation_notes = data.get('notes_mitigation')
            risk_entry.additional_mitigation = data.get(
                'additional_mitigation')
            # data.get('additional_mitigation')
            measurement_controls = []
            try:
                for item in EntryCompanyControl.objects.filter(id_entry_id=risk_entry.id):
                    item.delete()
            except:
                pass
            for request_data in payload:
                try:
                    control = CompanyControl.objects.get(
                        pk=request_data.get('company_id'))

                    entry_control = EntryCompanyControl.objects.create(
                        id_entry=risk_entry,
                        id_companycontrol=control,
                        sle_mitigation_rate=request_data.get(
                            'sle_mitigation_rate', 0) or 0,
                        aro_mitigation_rate=request_data.get(
                            'aro_mitigation_rate', 0) or 0
                    )
                    measurement_controls.append(
                        {'id': entry_control.id, 'name': entry_control.id_companycontrol.name})

                except:
                    rv = {'status': 'error', 'code': 400,
                          'errors': ["Invalid control"]}
            risk_entry.save()
            rv = {'status': 'success', 'code': 200, 'id': risk_entry.id,
                  "control": entry_control.id, "measurement_controls": measurement_controls}
        else:
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}
    except:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}

    return JsonResponse(rv)


@login_required
def api_update_measurements(request, entry_id):
    """Update threat entry."""
    try:
        if request.method == 'POST':
            risk_entry = Entry.objects.get(pk=entry_id)
            payload = json.loads(request.body.decode(
                'utf-8')).get("multidata", [])
            for request_data in payload:
                try:
                    control = EntryCompanyControl.objects.get(
                        id_entry=risk_entry, pk=request_data.get('control'))
                    selected_measurements = request_data.get("measurement", [])
                    for ecm in control.companycontrolmeasure_entry.all():
                        try:
                            selected_measurements.remove(
                                ecm.id_companycontrolmeasure)
                        except:
                            ecm.delete()
                    for measurement_id in selected_measurements:
                        measurement = CompanyControlMeasure.objects.get(
                            pk=measurement_id)
                        if measurement:
                            EntryCompanyControlMeasure.objects.create(
                                id_entrycompanycontrol=control, id_companycontrolmeasure=measurement)

                except:
                    rv = {'status': 'error', 'code': 400,
                          'errors': ["Invalid control"]}

            rv = {
                'status': 'success',
                'code': 200,
                'entry_details': {
                    'id': risk_entry.id,
                    'created_by': risk_entry.created_by.full_name,
                    'entry_date_created': risk_entry.date_created.strftime("%m-%d-%Y"),
                    'modified_by': risk_entry.modified_by.full_name,
                    'date_modified': risk_entry.date_modified.strftime("%m-%d-%Y"),
                    'mitigation_adequacy': risk_entry.evaluation.mitigation_adequacy if risk_entry.evaluation else '',
                    'date_evaluation': risk_entry.evaluation.date_evaluation if risk_entry.evaluation else '',
                    'total_asset_value': risk_entry.total_asset_value,
                    'total_control_mitigation': risk_entry.total_control_mitigation,
                }
            }
        else:
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}
    except:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}

    return JsonResponse(rv)


@login_required
def get_all_risk_type_for_dropdown(request):
    """Get all risk types for dropdown."""
    data = []
    for risk_type in RiskType.objects.order_by('sort_order').all():
        data.append({'id': risk_type.id, 'name': risk_type.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_responses_for_dropdown(request):
    """Get all respose types for dropdown."""
    data = []
    for response in Response.objects.order_by('sort_order').all():
        data.append({'id': response.id, 'name': response.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_time_units_for_dropdown(request):
    """Get all time units for dropdown."""
    data = []
    for unit in TimeUnit.objects.order_by('sort_order').all():
        data.append({'id': unit.id, 'name': unit.name,
                     'annual_units': unit.annual_units})
    return JsonResponse(data, safe=False)


@login_required
def get_all_frequencies_for_dropdown(request):
    """Get all frequency categories for dropdown."""
    data = []
    for frequency in FrequencyCategory.objects.order_by('sort_order').all():
        data.append({'id': frequency.id, 'name': frequency.name, 'desc': frequency.description,
                     'min': frequency.minimum, 'max': frequency.maximum})
    return JsonResponse(data, safe=False)


@login_required
def get_all_entry_urls_for_dropdown(request):
    """Get all entry urls for dropdown."""
    data = []
    for url in EntryUrl.objects.order_by('name').all():
        type = 'Internal'
        if url.is_internal == 0:
            type = 'External'
        data.append({'id': url.id, 'name': url.name, 'url': url.url,
                     'type': type, 'desc': url.description})
    return JsonResponse(data, safe=False)


@login_required
def get_all_compliance_types_for_dropdown(request):
    """Get all compliance types for dropdown."""
    data = []
    for type in ComplianceType.objects.order_by('sort_order').all():
        data.append({'id': type.id, 'name': type.name,
                     'desc': type.description})
    return JsonResponse(data, safe=False)


@login_required
def get_all_entry_company_control_for_dropdown(request):
    """Get all entry company control for dropdown."""
    data = []
    for measures in EntryCompanyControl.objects.select_related('id_companycontrol').order_by('name').all():
        data.append(
            {'id': measures.id, 'name': measures.id_companycontrol.name})
    return JsonResponse(data, safe=False)

@login_required
def get_all_ancillary_items_for_dropdown(request):
    """Get all ancillary items for dropdown."""
    data = []
    for item in EntryAncillaryType.objects.order_by('sort_order').all():
        data.append({'id': item.id, 'name': item.name})
    return JsonResponse(data, safe=False)


@login_required
def api_control_categories(request):
    """Get all control categories for dropdown."""
    data = []
    for item in ControlCategory.objects.order_by('sort_order').all():
        data.append({'id': item.id, 'name': item.name})
    return JsonResponse(data, safe=False)


@login_required
def api_get_company_contact(request):
    """Get all control contacts for dropdown."""
    company = request.user.get_current_company()
    data = []
    for item in CompanyContact.objects.filter(company_id=company):
        data.append({'id': item.id, 'name': item.first_name+item.last_name})
    return JsonResponse(data, safe=False)


@login_required
def api_save_new_vendor(request):
    """Save new Vendor."""
    company_id = request.user.get_current_company().id
    request_data = json.loads(request.body.decode('utf-8'))
    try:
        new_vendor = Vendor.objects.create(
            name=request_data.get('name'),
            url_main=request_data.get('url'),
            description=request_data.get('description'),
            company_id=company_id
        )
        rv = {
            'status': 'success',
            'code': 200,
            'new_vendor': {
                'id': new_vendor.id,
                'name': new_vendor.name,
                'url': new_vendor.url_main
            }
        }
    except:
        rv = {'status': 'error', 'code':400, 'errors': ["Invalid control"]}
    return JsonResponse(rv)

@login_required
def api_save_new_control(request, vendor_id):
    """Save new Control."""
    company_id = request.user.get_current_company().id
    request_data = json.loads(request.body.decode('utf-8'))
    try:
        new_control = Control.objects.create(
            name=request_data.get('name'),
            url=request_data.get('url'),
            company_id=company_id,
            vendor_id=vendor_id
        )
        ControlCategoryControl.objects.create(
            id_control_id=new_control.id,
            id_controlcategory_id=request_data.get('category')
        )
        rv = {
            'status': 'success',
            'code': 200,
            'new_control': {
                'id': new_control.id,
                'name': new_control.name,
                'category': request_data.get('category_name'),
                'url': new_control.url,
                'aka': '',
                'description': '',
                'abbrv': ''
            }
        }
    except:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid control"]}
    return JsonResponse(rv)

@login_required
def api_save_new_company_control(request):
    """Save New Company Control"""
    company_id = request.user.get_current_company().id
    request_data = json.loads(request.body.decode('utf-8'))
    try:
        date_maint = None
        try:
            date_maint = request_data.get('maintenance_date')[:10]
        except:
            pass

        estimated_maint_opex = 0
        recovery_multiplier = 0
        recovery_time_unit_id = None
        evaluation_days = 0
        poc_main_id = None
        poc_support_id = None
        try:
            estimated_maint_opex = Decimal(float(request_data.get('opex')))
        except:
            pass

        try:
            recovery_multiplier = int(request_data.get('recovery_multiplier'))
        except:
            pass

        try:
            recovery_time_unit_id = int(request_data.get('recovery_time_unit'))
        except:
            pass

        try:
            evaluation_days = int(request_data.get('evaluation_days'))
        except:
            pass

        try:
            poc_main_id = int(request_data.get('poc_main'))
        except:
            pass

        try:
            poc_support_id = int(request_data.get('poc_support'))
        except:
            pass

        cc_id = request_data.get('id')
        if cc_id is None:
            cc = CompanyControl.objects.create(
                company_id=company_id,
                control_id=request_data.get('control_id'),
                name=request_data.get('name'),
                alias=request_data.get('alias'),
                description=request_data.get('description'),
                version=request_data.get('version'),
                estimated_maint_opex=estimated_maint_opex,
                opex_description=request_data.get('opex_desc'),
                date_maint=date_maint,
                recovery_multiplier=recovery_multiplier,
                recovery_time_unit_id=recovery_time_unit_id,
                evaluation_days=evaluation_days,
                poc_main_id=poc_main_id,
                poc_support_id=poc_support_id
            )
        else:
            cc = CompanyControl.objects.get(pk=cc_id)
            cc.control_id = request_data.get('control_id')
            cc.name = request_data.get('name')
            cc.alias = request_data.get('alias')
            cc.description = request_data.get('description')
            cc.version = request_data.get('version')
            cc.estimated_maint_opex = estimated_maint_opex
            cc.opex_description = request_data.get('opex_desc')
            cc.date_maint = date_maint
            cc.recovery_multiplier = recovery_multiplier
            cc.recovery_time_unit_id = recovery_time_unit_id
            cc.evaluation_days = evaluation_days
            cc.poc_main_id = poc_main_id
            cc.poc_support_id = poc_support_id
            cc.save()

        selected_locations = request_data.get('company_locations', [])
        try:
            for ccl in CompanyControlLocation.objects.filter(id_companycontrol_id=cc_id):
                try:
                    selected_locations.remove(ccl.id)
                except:
                    ccl.delete()
        except:
            print(traceback.format_exc())
            pass
        try:
            for location in selected_locations:
                try:
                    CompanyControlLocation.objects.create(
                        id_companycontrol_id=cc.id,
                        id_companylocation_id=location
                    )
                except:
                    pass
        except:
            pass

        selected_segments = request_data.get('company_segments',[])
        try:
            for ccs in CompanyControlSegment.objects.filter(id_companycontrol_id=cc_id):
                try:
                    selected_segments.remove(ccs.id)
                except:
                    ccs.delete()
        except:
            pass
        try:
            for segment in selected_segments:
                try:
                    CompanyControlSegment.objects.create(
                        id_companycontrol_id=cc.id,
                        id_companysegment_id=segment
                    )
                except:
                    pass
        except:
            pass
        rv = {
            'status': 'success',
            'code': 200
        }
    except:
        print(traceback.format_exc())
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid control"]}
    return JsonResponse(rv)

@login_required
def api_get_risk_entry(request, entry_id):
    """Get risk entry by id."""
    rv = {}
    if entry_id:
        try:
            # Get first register for company from entry.py/Register
            risk_entry = request.user.get_current_company(
            ).get_active_register().entry.get(pk=entry_id)
            compliance_requirements = []
            try:
                for entry_compliance_requirement in EntryComplianceRequirement.objects.filter(id_entry_id=risk_entry.id):
                    compliance_requirement = ComplianceRequirement.objects.get(
                        pk=entry_compliance_requirement.id_compliance_requirement_id)
                    compliance = Compliance.objects.get(
                        pk=compliance_requirement.compliance_id)

                    compliance_requirements.append({
                        'type_id': compliance.compliance_type_id,
                        'type': ComplianceType.objects.get(id=compliance.compliance_type_id).name,
                        'name': compliance.abbrv,
                        'compliance_id': compliance.id,
                        'requirement': str(compliance_requirement.cid) + ' - ' + compliance_requirement.requirement,
                        'requirement_id': compliance_requirement.id,
                        'version': ''
                    })
            except:
                pass

            entry_urls = []
            try:
                for entry_url in EntryUrl.objects.filter(entry_id=risk_entry.id):
                    entry_urls.append({
                        'url': entry_url.url,
                        'name': entry_url.name,
                        'type': '1' if entry_url.is_internal else '0',
                        'type_name': 'Internal' if entry_url.is_internal else 'External',
                        'desc': entry_url.description
                    })
            except:
                pass

            artifacts_files = []
            try:
                for artifact_file in EntryCompanyArtifact.objects.filter(id_entry_id=risk_entry.id):
                    company_artifact = CompanyArtifact.objects.get(
                        pk=artifact_file.id_companyartifact_id)
                    artifacts_files.append({
                        'entry_company_artifact_id': artifact_file.id,
                        'name': company_artifact.name,
                        'desc': company_artifact.description,
                        'file': {
                            'name': company_artifact.artifact_file.name.split('/')[-1],
                            'path': company_artifact.artifact_file.name
                        }
                    })
            except:
                pass
            rv.update({
                'basicinfo': {
                    'entry_id': risk_entry.id,
                    'summary': risk_entry.summary,
                    'description': risk_entry.description,
                    'assumption': risk_entry.assumption,
                    'locations': [loc.id_companylocation_id for loc in risk_entry.entry_companylocation.all()] or [1, ],
                    'response': risk_entry.response_id,
                    'entry_owner': risk_entry.entry_owner_id or request.user.id,
                    'evaluation_days': risk_entry.evaluation_days,
                    'aro_toggle': risk_entry.aro_toggle,
                    'aro_known_multiplier': risk_entry.aro_known_multiplier,
                    'aro_known_unit_quantity': risk_entry.aro_known_unit_quantity,
                    'aro_time_unit': risk_entry.aro_time_unit_id,
                    'aro_frequency': risk_entry.aro_frequency_id,
                    'aro_fixed': float(risk_entry.aro_fixed),
                    'aro_notes': risk_entry.aro_notes,
                    'compliance_requirements': compliance_requirements,
                    'entry_urls': entry_urls,
                    'artifacts_files': artifacts_files,
                    'incident_response': '1' if risk_entry.incident_response else '0'
                }
            })

            try:
                threat_details = []
                for entry_actor in risk_entry.actor_entry.order_by('id').all():
                    selected_intentions = ''
                    for intention in entry_actor.intentions.all():
                        selected_intentions += intention.name + '\n'
                    selected_motives = ''
                    for motive in entry_actor.motives.all():
                        selected_motives += motive.name + '\n'
                    threat_details.append({
                        'entry_actor_id': entry_actor.id,
                        'actor_name_id': entry_actor.id_actor_id,
                        'actor_name': Actor.objects.get(id=entry_actor.id_actor_id).name,
                        'intentions_id': [iea.id for iea in entry_actor.intentions.all()],
                        'intentions': selected_intentions,
                        'motives_id': [iea.id for iea in entry_actor.motives.all()],
                        'motives': selected_motives,
                        'detail': entry_actor.detail,
                    })

                rv.update({'threat_details': {'multidata': threat_details}})

            except:
                pass

            aro_rate = 0
            if risk_entry.aro_toggle == 'C':
                frequency_category = FrequencyCategory.objects.get(
                    id=risk_entry.aro_frequency_id)
                aro_rate = (frequency_category.minimum +
                            frequency_category.maximum) / 2 * 100
                if frequency_category.minimum == 1:
                    aro_rate = 100
            elif risk_entry.aro_toggle == 'K':
                aro_rate = risk_entry.aro_fixed
            else:
                time_unit = TimeUnit.objects.get(
                    id=risk_entry.aro_time_unit_id)
                aro_rate = risk_entry.aro_known_multiplier * \
                    time_unit.annual_units / risk_entry.aro_known_unit_quantity
                if aro_rate >= 1:
                    aro_rate = 100
                else:
                    aro_rate *= 100

            aro_rate = risk_entry.get_aro_rate()
            aro_rate = Decimal(aro_rate)

            total_cost_value_an = 0
            total_ale_value_an = 0
            try:
                ancillary_items = []
                for item in EntryAncillary.objects.filter(entry=risk_entry):
                    ancillary_items.append({
                        'type_id': item.ancillary_type_id,
                        'type': EntryAncillaryType.objects.get(id=item.ancillary_type_id).name,
                        'summary': item.summary,
                        'description': item.description,
                        'detail': item.cost_detail,
                        'evaluation_days': item.evaluation_days,
                        'cost': item.ancillary_fixed,
                        'occurences': item.per_occurance,
                        'total_cost': item.per_occurance * item.ancillary_fixed
                    })
                    total_cost_value_an += float(item.per_occurance * item.ancillary_fixed)
                    total_ale_value_an += float(item.per_occurance * item.ancillary_fixed) * float(aro_rate) / 100
                rv.update({
                    'ancillary_items': {
                        'multidata': ancillary_items,
                        'total_cost_value': total_cost_value_an
                    }
                })
            except:
                pass


            total_sle = 0
            total_ale = 0
            try:
                affected_assets = []
                total_asset_value = 0
                for entry_company_asset in risk_entry.companyasset_entry.order_by('id').all():
                    company_asset = CompanyAsset.objects.get(
                        pk=entry_company_asset.id_companyasset_id)
                    sle_value = round(Decimal(company_asset.get_asset_value()) * Decimal(entry_company_asset.exposure_factor_rate) / 100,
                                      2) if entry_company_asset.exposure_factor_toggle == 'P' else round(entry_company_asset.exposure_factor_fixed, 2)
                    ale_value = round(Decimal(company_asset.get_asset_value()) * Decimal(entry_company_asset.exposure_factor_rate) * aro_rate / 10000,
                                      2) if entry_company_asset.exposure_factor_toggle == 'P' else round(Decimal(entry_company_asset.exposure_factor_fixed) * aro_rate / 100, 2)
                    total_asset_value += round(
                        company_asset.get_asset_value(), 2)
                    total_sle += sle_value
                    total_ale += ale_value
                    affected_assets.append({
                        'entry_asset_id': entry_company_asset.id,
                        'name_id': company_asset.id,
                        'name': company_asset.name,
                        'exposure_factor_toggle': entry_company_asset.exposure_factor_toggle,
                        'asset_value': round(company_asset.get_asset_value(), 2),
                        'exposure_factor_fixed': round(entry_company_asset.exposure_factor_fixed, 2),
                        'exposure_factor_rate': round(entry_company_asset.exposure_factor_rate, 2),
                        'asset_value_display': round(company_asset.get_asset_value(), 2),
                        'factor': 'rate: ' + str(round(entry_company_asset.exposure_factor_rate, 3)) + '%' if entry_company_asset.exposure_factor_toggle == 'P' else 'fixed: $' + str(round(entry_company_asset.exposure_factor_fixed, 2)),
                        'detail': entry_company_asset.detail,
                        'sle_value': sle_value,  # Need to validate the use of this value
                        'sle': sle_value,
                        'ale_value': ale_value,  # Need to validate the use of this value
                        'ale': ale_value
                    })
                try:
                    total_factor = round(total_sle / total_asset_value * 100, 2)
                except:
                    total_factor = total_sle
                    print("total_factor Calc error")
                    pass
                rv.update({
                    'affected_assets': {
                        'multidata': affected_assets,
                        'total_asset_value': round(total_asset_value, 2),
                        'total_factor_value': total_factor,
                        'total_factor': str(total_factor) + '%',
                        'total_sle_value': total_sle,  # Need to validate the use of this value
                        'total_sle': total_sle,
                        'total_ale_value': total_ale,  # Need to validate the use of this value
                        'total_ale': total_ale,
                        'total_ale_with_ancillary': total_ale + Decimal(total_ale_value_an)
                    }
                })
            except:
                print(traceback.format_exc())
                pass

            total_sle += Decimal(total_cost_value_an)
            try:
                mitigating_controls = []
                total_sle_rate = 0
                for mitigating_control in risk_entry.companycontrol_entry.order_by('id').all():
                    total_sle_rate += mitigating_control.sle_mitigation_rate
                total_sle_rate = Decimal(total_sle_rate)
                total_aro_rate = 0
                total_sle_cost = 0
                total_aro_cost = 0
                total_cost = 0
                total_ale = 0
                for mitigating_control in risk_entry.companycontrol_entry.order_by('id').all():
                    company_control = CompanyControl.objects.get(
                        pk=mitigating_control.id_companycontrol_id)
                    company = Company.objects.get(
                        pk=company_control.company_id)
                    control = Control.objects.get(
                        pk=company_control.control_id)
                    vendor = Vendor.objects.get(pk=control.vendor_id)
                    sle_cost_value = round(
                        total_sle * Decimal(mitigating_control.sle_mitigation_rate) / 100, 2)
                    aro_cost_value = round(
                        total_sle * (100 - total_sle_rate) * Decimal(mitigating_control.aro_mitigation_rate) / 10000, 2)
                    total_cost_value = sle_cost_value + aro_cost_value
                    total_ale_impact_value = round(
                        total_cost_value * aro_rate / 100, 2)
                    total_sle_cost += sle_cost_value
                    total_aro_cost += aro_cost_value
                    total_cost += total_cost_value
                    total_ale += total_ale_impact_value
                    total_aro_rate += mitigating_control.aro_mitigation_rate
                    mitigating_controls.append({
                        'entry_company_control_id': mitigating_control.id,
                        'company_id': company_control.id,
                        'company_name': company_control.name,
                        'control_name': control.name,
                        'vendor_name': vendor.name,
                        'max_loss': company.get_company_max_loss(),
                        'sle_mitigation_rate': mitigating_control.sle_mitigation_rate,
                        'sle_rate': mitigating_control.sle_mitigation_rate,
                        'sle_rate_display': str(mitigating_control.sle_mitigation_rate) + '%',
                        'aro_mitigation_rate': mitigating_control.aro_mitigation_rate,
                        'aro_rate': mitigating_control.aro_mitigation_rate,
                        'aro_rate_display': str(mitigating_control.aro_mitigation_rate) + '%',
                        'sle_cost_value': sle_cost_value,  # Need to validate the use of this value
                        'sle_cost': sle_cost_value,
                        'aro_cost_value': aro_cost_value,
                        'aro_cost': aro_cost_value,  # Need to validate the use of this value
                        'total_cost_value': total_cost_value,
                        'total_cost': total_cost_value,
                        'total_ale_impact_value': total_ale_impact_value,
                        'total_ale_impact': total_ale_impact_value,
                        'notes': mitigating_control.notes
                    })

                rv.update({
                    'mitigating_controls': {
                        'multidata': mitigating_controls,
                        'sle_rate': total_sle_rate,
                        'sle_cost': total_sle_cost,
                        'aro_rate': total_aro_rate,
                        'aro_cost': total_aro_cost,
                        'total_cost': total_cost,
                        'total_ale': total_ale,
                        'notes_mitigation': risk_entry.mitigation_notes,
                        'additional_mitigation': risk_entry.additional_mitigation
                    }
                })
            except:
                pass
        except:
            print(traceback.format_exc())
            pass

    return JsonResponse(rv)


@login_required
def api_list_entries_info(request):
    """Get Detailed information for Entry list."""
    data = {}
    company_residual_ale_rate = 0
    highest_total_ale = 0
    highest_residual_ale_cost = 0
    protection_residual_ale_cost_sum = 0
    protection_inherent_ale_cost_sum = 0
    protection_inherent_ale_cost_sum_qualified_and_treat = 0
    protection_mitigated_ale_cost_sum_qualified_and_treat = 0
    count_active_entries = 0
    count_treat_entries = 0
    count_transfer_entries = 0
    count_accept_entries = 0
    count_avoid_entries = 0
    count_qualified_entries = 0
    count_not_completed_entries = 0
    count_require_evaluation_entries = 0
    rate_relation = {}
    user = request.user
    try:
        company = user.get_current_company()
        # Get fist register for company from entry.py/Register
        company_register = company.get_active_register()
        register_entries = company_register.entry
        total = register_entries.count()
        for entry in register_entries.order_by('id').all():
            # ARO Rate
            aro_rate = 0
            if entry.aro_toggle == 'C':
                frequency_category = FrequencyCategory.objects.get(
                    id=entry.aro_frequency_id)
                rate_relation = {
                    'minimum': frequency_category.minimum,
                    'maximum': frequency_category.maximum
                }
                aro_rate = (frequency_category.minimum +
                            frequency_category.maximum) / 2 * 100
                if frequency_category.minimum == 1:
                    aro_rate = 100
            elif entry.aro_toggle == 'K':
                aro_rate = entry.aro_fixed
            else:
                time_unit = TimeUnit.objects.get(
                    id=entry.aro_time_unit_id)
                rate_relation = {
                    'annual_units': time_unit.annual_units
                }
                aro_rate = entry.aro_known_multiplier * \
                    time_unit.annual_units / entry.aro_known_unit_quantity
                if aro_rate >= 1:
                    aro_rate = 100
                else:
                    aro_rate *= 100

            aro_rate = entry.get_aro_rate()
            aro_rate = Decimal(aro_rate)
            # Total SLE
            total_sle = 0
            total_ale = 0
            try:
                total_asset_value = 0
                for entry_company_asset in entry.companyasset_entry.order_by('id').all():
                    company_asset = CompanyAsset.objects.get(
                        pk=entry_company_asset.id_companyasset_id)
                    sle_value = round(
                        Decimal(company_asset.get_asset_value()) *
                        Decimal(entry_company_asset.exposure_factor_rate) / 100,
                        2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                        entry_company_asset.exposure_factor_fixed, 2)
                    ale_value = round(Decimal(company_asset.get_asset_value()) * Decimal(
                        entry_company_asset.exposure_factor_rate) * aro_rate / 10000,
                        2) if entry_company_asset.exposure_factor_toggle == 'P' else round(
                        Decimal(entry_company_asset.exposure_factor_fixed) * aro_rate / 100, 2)
                    total_asset_value += round(
                        company_asset.get_asset_value(), 2)
                    total_sle += sle_value
                    total_ale += ale_value
            except:
                pass
            # Mitigating Info
            total_ale_impact = 0
            try:
                total_sle_rate = 0
                for mitigating_control in entry.companycontrol_entry.order_by('id').all():
                    total_sle_rate += mitigating_control.sle_mitigation_rate
                total_sle_rate = Decimal(total_sle_rate)
                total_aro_rate = 0
                total_sle_cost = 0
                total_aro_cost = 0
                total_cost = 0
                for mitigating_control in entry.companycontrol_entry.order_by('id').all():
                    company_control = CompanyControl.objects.get(
                        pk=mitigating_control.id_companycontrol_id)
                    company = Company.objects.get(
                        pk=company_control.company_id)
                    control = Control.objects.get(
                        pk=company_control.control_id)
                    vendor = Vendor.objects.get(pk=control.vendor_id)
                    sle_cost_value = round(
                        total_sle * Decimal(mitigating_control.sle_mitigation_rate) / 100, 2)
                    aro_cost_value = round(
                        total_sle * (100 - total_sle_rate) * Decimal(mitigating_control.aro_mitigation_rate) / 10000, 2)
                    total_cost_value = sle_cost_value + aro_cost_value
                    impact_value = round(total_cost_value * aro_rate / 100, 2)
                    total_sle_cost += sle_cost_value
                    total_aro_cost += aro_cost_value
                    total_cost += total_cost_value
                    total_ale_impact += impact_value
                    total_aro_rate += mitigating_control.aro_mitigation_rate
            except:
                pass
            highest_total_ale = total_ale if total_ale > highest_total_ale and entry.is_qualified(
                rate_relation) else highest_total_ale
            highest_residual_ale_cost = Decimal(total_ale - total_ale_impact) if Decimal(
                total_ale - total_ale_impact) > highest_residual_ale_cost and entry.is_qualified(rate_relation) else highest_residual_ale_cost
            company_residual_ale_rate += Decimal(
                total_ale - total_ale_impact) if entry.is_qualified(rate_relation) else 0
            protection_inherent_ale_cost_sum += total_ale if entry.response_name == 'Treat' else 0
            protection_residual_ale_cost_sum += Decimal(
                total_ale - total_ale_impact) if entry.response_name == 'Treat' else 0
            protection_mitigated_ale_cost_sum_qualified_and_treat += total_ale_impact if entry.response_name == 'Treat' and entry.is_qualified(
                rate_relation) else 0
            protection_inherent_ale_cost_sum_qualified_and_treat += total_ale if entry.response_name == 'Treat' and entry.is_qualified(
                rate_relation) else 0
            count_active_entries += 1 if entry.is_active == 1 else 0
            count_treat_entries += 1 if entry.response_name == 'Treat' else 0
            count_transfer_entries += 1 if entry.response_name == 'Transfer' else 0
            count_accept_entries += 1 if entry.response_name == 'Accept' else 0
            count_avoid_entries += 1 if entry.response_name == 'Avoid' else 0
            count_qualified_entries += 1 if entry.is_qualified(
                rate_relation) else 0
            count_not_completed_entries += 0 if entry.has_completed(
                rate_relation) else 1
            count_require_evaluation_entries += 1 if entry.evaluation_flg else 0

        try:
            company_residual_ale_rate = round(company_residual_ale_rate / Decimal(
                request.user.get_current_company().get_company_max_loss()) * 100, 5)
        except:
            company_residual_ale_rate = 0
        try:
            protection_rate = round(
                protection_residual_ale_cost_sum / protection_inherent_ale_cost_sum * 100, 5)
        except:
            protection_rate = 0

        company_residual_ale_rate_width = str(company_residual_ale_rate) + '%'
        treated_entry_protection_width = str(protection_rate) + '%'
        count_active_entries_width = str(
            count_active_entries / total * 100) + '%'
        count_qualified_entries_width = str(
            count_qualified_entries / total * 100) + '%'
        data = {
            'company_residual_ale_rate': company_residual_ale_rate,
            'company_residual_ale_rate_width': company_residual_ale_rate_width,
            'highest_total_ale': highest_total_ale,
            'highest_residual_ale_cost': highest_residual_ale_cost,
            'treated_entry_protection': protection_rate,
            'treated_entry_protection_width': treated_entry_protection_width,
            'mitigated_ale_total': protection_mitigated_ale_cost_sum_qualified_and_treat,
            'inherent_ale_total': protection_inherent_ale_cost_sum_qualified_and_treat,
            'count_active_entries': count_active_entries,
            'count_active_entries_width': count_active_entries_width,
            'count_treat_entries': count_treat_entries,
            'count_transfer_entries': count_transfer_entries,
            'count_accept_entries': count_accept_entries,
            'count_avoid_entries': count_avoid_entries,
            'count_qualified_entries': count_qualified_entries,
            'count_qualified_entries_width': count_qualified_entries_width,
            'count_not_completed_entries': count_not_completed_entries,
            'count_require_evaluation_entries': count_require_evaluation_entries
        }
    except:
        print(traceback.format_exc())
        pass
    return JsonResponse(data, safe=False)



@login_required
def api_delete_company_control(request, cc_id):
    """Delete Company Control by id"""
    company = request.user.get_current_company()
    rv = {}
    if cc_id:
        try:
            for e_cc in EntryCompanyControl.objects.filter(id_companycontrol_id=cc_id):
                try:
                    e_cc.delete()
                except:
                    pass
            CompanyControlLocation.objects.filter(id_companycontrol_id=cc_id).delete()
            CompanyControlSegment.objects.filter(id_companycontrol_id=cc_id).delete()
            CompanyControl.objects.get(id=cc_id).delete()
            rv = {
                'status': 'success',
                'code': 200
            }
        except:
            print(traceback.format_exc())
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid control"]}
    return JsonResponse(rv)

@login_required
def api_delete_company_asset(request, ca_id):
    """Delete Company Asset by id"""
    company = request.user.get_current_company()
    rv = {}
    if ca_id:
        try:
            for e_ca in EntryCompanyAsset.objects.filter(id_companyasset_id=ca_id):
                try:
                    e_ca.delete()
                except:
                    pass
            CompanyAssetLocation.objects.filter(id_companyasset_id=ca_id).delete()
            CompanyAsset.objects.get(id=ca_id).delete()
            rv = {
                'status': 'success',
                'code': 200
            }
        except:
            print(traceback.format_exc())
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid control"]}
    return JsonResponse(rv)