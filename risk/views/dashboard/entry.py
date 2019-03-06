"""All views related to Entry in models/entry.py."""
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.views import View
from decimal import *
from risk.models import (
    Actor,
    ActorIntent,
    ActorMotive,
    CompanyAsset,
    CompanyControl,
    CompanyControlMeasure,
    CompanyLocation,
    Compliance,
    Entry,
    EntryActor,
    EntryActorIntent,
    EntryActorMotive,
    EntryCompanyAsset,
    EntryCompanyControl,
    EntryCompanyControlMeasure,
    EntryCompanyLocation,
    EntryCompliance,
    EntryResponseSubmission,
    EntryRiskType,
    Response,
    RiskType,
    TimeUnit,
    FrequencyCategory,
    EntryUrl,
    ComplianceType,
    ComplianceRequirement,
    EntryComplianceRequirement,
    CompanyAsset,
    SeverityCategory,
    Company,
    Control,
    Vendor
)
from risk.forms.entry import(
    RiskEntryBasicForm,
)


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
        for entry in register_entries.order_by('-date_modified').all():
            category_name = ''
            try:
                for category in SeverityCategory.objects.order_by('name').all():
                    if float(entry.residual_ale_rate) >= category.minimum and float(entry.residual_ale_rate) < category.maximum:
                        category_name = category.name
                if int(entry.residual_ale_rate) >= 1:
                    category_name = 'Critical'
            except:
                pass
            rows.append({
                'owner_name': entry.entry_owner.full_name,
                'compliance': entry.has_compliance,
                'completed': entry.has_completed,
                'entry_number': entry.id,  # Entry number
                'response': entry.response_name,
                'mr': entry.mitigation_rate,  #
                'residual_ale_category': category_name,  #
                'residual_ale_rate': round(entry.residual_ale_rate, 5),
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
        data = {

        }
    return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class CreateRiskEntry(View):
    """Create Risk Entry."""

    form_class = RiskEntryBasicForm

    def post(self, request, *args, **kwargs):
        """Handle post requests."""
        request_data = json.loads(request.body.decode('utf-8'))

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
            risk_entry.aro_frequency_id = int(
                request_data.get("aro_frequency", request.user.id))
            risk_entry.aro_time_unit_id = int(
                request_data.get("aro_time_unit", request.user.id))
            risk_entry.modified_by = request.user
            risk_entry.save()

            # Select single dropdown
            # try:
            #     risk_entry.response_id = int(
            #       request_data.get("response", request.response.id))
            #     try:
            #         entry_response = EntryResponse.objects.filter(
            #             entry=risk_entry).latest('id')
            #         entry_response.response = response
            #         entry_response.save()
            #     except:
            #         EntryResponse.objects.create(
            #             entry=risk_entry, response=response)
            # except:
            #     pass

            # Select multiple dropdowns - Risk Type
            # selected_rt = request_data.get("risk_types", [])
            # for ert in risk_entry.entryrisktype.all():
            #     try:
            #         selected_rt.remove(ert.id_risktype_id)
            #     except:  # This risktype is not selected anymore
            #         ert.delete()
            # # Add new RiskType
            # for risk_type_id in selected_rt:
            #     try:
            #         risk_type = RiskType.objects.get(pk=risk_type_id)
            #         EntryRiskType.objects.get_or_create(
            #             id_entry=risk_entry, id_risktype=risk_type)
            #     except:
            #         pass

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

            # Select multiple dropdowns - Compliance
            # selected_cp = request_data.get("compliances", [])
            # for ecp in risk_entry.entrycompliance.all():
            #     try:
            #         selected_cp.remove(ecp.id_compliance_id)
            #     except:  # This Compliance is not selected anymore
            #         ecp.delete()
            # Add new Compliance
            # for compliances_id in selected_cp:
            #     try:
            #         compliance = Compliance.objects.get(pk=compliances_id)
            #         EntryCompliance.objects.get_or_create(
            #             id_entry=risk_entry, id_compliance=compliance)
            #     except:
            #         pass
            # Compliance Requirements
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
            entry_urls = request_data.get("entry_urls", [])
            for entry_url in entry_urls:
                try:
                    EntryUrl.objects.get_or_create(
                        entry=risk_entry, url=entry_url['url'], description=entry_url['desc'], name=entry_url['name'], is_internal=entry_url['type'])
                except:
                    pass
            rv = {'status': 'success', 'code': 200, 'id': risk_entry.id, 'created_date': risk_entry.date_created.strftime(
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
            for request_data in payload:
                try:
                    actor = Actor.objects.get(
                        pk=request_data.get('actor_name_id'))
                    # Get current entry actor (if any)
                    try:  # If EntryActor already exists
                        entry_actor_id = request_data.get('entry_actor_id')
                        entry_actor = EntryActor.objects.get(
                            id=entry_actor_id, id_entry=risk_entry)
                        entry_actor.id_actor = actor
                        entry_actor.detail = request_data.get('detail')
                        entry_actor.save()
                    except:  # No actor already, create one
                        entry_actor = EntryActor.objects.create(
                            id_entry=risk_entry, id_actor=actor, detail=request_data.get('detail'))

                    # Select multiple dropdowns - Intensions
                    selected_intents = request_data.get("intentions_id", [])
                    for ai in entry_actor.intent_entryactor.all():
                        try:
                            selected_intents.remove()
                        except:
                            ai.delete()
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
                    for am in entry_actor.motive_entryactor.all():
                        try:
                            selected_motives.remove()
                        except:
                            am.delete()

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
            for request_data in payload:
                # Get current company asset (if any)
                try:
                    asset = CompanyAsset.objects.get(
                        pk=int(request_data.get('name_id')))
                    toggle = request_data.get('exposure_factor_toggle')
                    entry_asset_id = request_data.get('entry_asset_id')
                    try:
                        entry_asset = EntryCompanyAsset.objects.get(
                            id=entry_asset_id, id_entry=risk_entry)
                        entry_asset.id_companyasset = asset
                        entry_asset.detail = request_data.get('detail')
                        entry_asset.exposure_factor_toggle = toggle
                        entry_asset.exposure_factor_fixed = 0 if toggle == 'P' else request_data.get('exposure_factor_fixed')
                        entry_asset.exposure_factor_rate = 0 if toggle == 'F' else request_data.get('exposure_factor_rate')
                        entry_asset.exposure_factor = request_data.get('exposure_factor')
                        entry_asset.save()
                    except:
                        EntryCompanyAsset.objects.create(
                            id_entry=risk_entry,
                            id_companyasset=asset,
                            detail=request_data.get('detail'),
                            exposure_factor_toggle=toggle,
                            exposure_factor_fixed=0 if toggle == 'P' else request_data.get('exposure_factor_fixed'),
                            exposure_factor_rate=0 if toggle == 'F' else request_data.get('exposure_factor_rate')
                        )
                except:
                    rv = {'status': 'error', 'code': 400,
                          'errors': ["Invalid asset"]}
            # risk_entry.mitigation_notes = data.get('mitigation_notes')
            # risk_entry.save()

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
            risk_entry.additional_mitigation = data.get('additional_mitigation')
            # data.get('additional_mitigation')
            measurement_controls = []
            for request_data in payload:
                try:
                    control = CompanyControl.objects.get(pk=request_data.get('company_id'))
                    entry_mcontrol_id = request_data.get('entry_company_control_id')
                    try:
                        entry_control = EntryCompanyControl.objects.get(
                            id=entry_mcontrol_id, id_entry=risk_entry)
                        entry_control.id_companycontrol = control
                        entry_control.sle_mitigation_rate = request_data.get('sle_mitigation_rate', 0) or 0
                        entry_control.aro_mitigation_rate = request_data.get('aro_mitigation_rate', 0) or 0
                        entry_control.notes = request_data.get('notes')
                        entry_control.save()
                    except:
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
    for risk_type in RiskType.objects.order_by('name').all():
        data.append({'id': risk_type.id, 'name': risk_type.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_responses_for_dropdown(request):
    """Get all respose types for dropdown."""
    data = []
    for response in Response.objects.order_by('name').all():
        data.append({'id': response.id, 'name': response.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_time_units_for_dropdown(request):
    """Get all time units for dropdown."""
    data = []
    for unit in TimeUnit.objects.order_by('name').all():
        data.append({'id': unit.id, 'name': unit.name,
                     'annual_units': unit.annual_units})
    return JsonResponse(data, safe=False)


@login_required
def get_all_frequencies_for_dropdown(request):
    """Get all frequency categories for dropdown."""
    data = []
    for frequency in FrequencyCategory.objects.order_by('name').all():
        data.append({'id': frequency.id, 'name': frequency.name,
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
    for type in ComplianceType.objects.order_by('name').all():
        data.append({'id': type.id, 'name': type.name})
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
def api_get_risk_entry(request, entry_id):
    """Get risk entry by id."""
    rv = {}
    if entry_id:
        try:
            # Get first register for company from entry.py/Register
            risk_entry = request.user.get_current_company(
            ).get_active_register().entry.get(pk=entry_id)
            # try:
            #     response = risk_entry.entryresponse.latest(
            #         'id').response_id
            # except:
            #     response = 1
            compliance_requirements = []
            for entry_compliance_requirement in EntryComplianceRequirement.objects.filter(id_entry_id=risk_entry.id):
                compliance_requirement = ComplianceRequirement.objects.get(
                    pk=entry_compliance_requirement.id_compliance_requirement_id)
                compliance = Compliance.objects.get(
                    pk=compliance_requirement.compliance_id)

                compliance_requirements.append({
                    'type_id': compliance.compliance_type_id,
                    'type': ComplianceType.objects.get(id=compliance.compliance_type_id).name,
                    'name': compliance.name,
                    'compliance_id': compliance.id,
                    'requirement': compliance_requirement.requirement,
                    'requirement_id': compliance_requirement.id,
                    'version': ''
                })

            entry_urls = []
            for entry_url in EntryUrl.objects.filter(entry_id=risk_entry.id):
                entry_urls.append({
                    'url': entry_url.url,
                    'name': entry_url.name,
                    'type': '1' if entry_url.is_internal else '0',
                    'type_name': 'Internal' if entry_url.is_internal else 'External',
                    'desc': entry_url.description
                })
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
                    'aro_fixed': int(risk_entry.aro_fixed),
                    'aro_notes': risk_entry.aro_notes,
                    'compliance_requirements': compliance_requirements,
                    'entry_urls': entry_urls,
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
                aro_rate = risk_entry.aro_known_multiplier * time_unit.annual_units / risk_entry.aro_known_unit_quantity
                if aro_rate >= 1:
                    aro_rate = 100
                else:
                    aro_rate *= 100
            aro_rate = Decimal(aro_rate)
            try:
                affected_assets = []
                total_asset_value = 0
                total_sle = 0
                total_ale = 0
                for entry_company_asset in risk_entry.companyasset_entry.order_by('id').all():
                    company_asset = CompanyAsset.objects.get(
                        pk=entry_company_asset.id_companyasset_id)
                    sle_value = round(Decimal(company_asset.asset_value_fixed) * Decimal(entry_company_asset.exposure_factor_rate) / 100,
                                      3) if entry_company_asset.exposure_factor_toggle == 'P' else round(entry_company_asset.exposure_factor_fixed, 3)
                    ale_value = round(Decimal(company_asset.asset_value_fixed) * Decimal(entry_company_asset.exposure_factor_rate) * aro_rate / 10000,
                                      3) if entry_company_asset.exposure_factor_toggle == 'P' else round(Decimal(entry_company_asset.exposure_factor_fixed) * aro_rate / 100, 3)
                    total_asset_value += round(company_asset.asset_value_fixed, 3)
                    total_sle += sle_value
                    total_ale += ale_value
                    affected_assets.append({
                        'entry_asset_id': entry_company_asset.id,
                        'name_id': company_asset.id,
                        'name': company_asset.name,
                        'exposure_factor_toggle': entry_company_asset.exposure_factor_toggle,
                        'asset_value': round(company_asset.asset_value_fixed, 3),
                        'exposure_factor_fixed': round(entry_company_asset.exposure_factor_fixed, 3),
                        'exposure_factor_rate': int(entry_company_asset.exposure_factor_rate),
                        'asset_value_display': '$' + str(round(company_asset.asset_value_fixed, 3)),
                        'factor': 'rate: ' + str(round(entry_company_asset.exposure_factor_rate, 3)) + '%' if entry_company_asset.exposure_factor_toggle == 'P' else 'fixed: $' + str(round(entry_company_asset.exposure_factor_fixed, 3)),
                        'detail': entry_company_asset.detail,
                        'sle_value': sle_value,
                        'sle': '$' + str(sle_value),
                        'ale_value': ale_value,
                        'ale': '$' + str(ale_value)
                    })
                total_factor = round(total_sle / total_asset_value * 100, 3)
                rv.update({
                    'affected_assets': {
                        'multidata': affected_assets,
                        'total_asset_value': '$' + str(total_asset_value),
                        'total_factor_value': total_factor,
                        'total_factor': str(total_factor) + '%',
                        'total_sle_value': total_sle,
                        'total_sle': '$' + str(total_sle),
                        'total_ale_value': total_ale,
                        'total_ale': '$' + str(total_ale)
                    }
                })
            except:
                pass

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
                        total_sle * Decimal(mitigating_control.sle_mitigation_rate) / 100, 3)
                    aro_cost_value = round(
                        total_sle * (100 - total_sle_rate) * Decimal(mitigating_control.aro_mitigation_rate) / 10000, 3)
                    total_cost_value = sle_cost_value + aro_cost_value
                    total_ale_impact_value = round(total_cost_value * aro_rate / 100, 3)
                    total_sle_cost += sle_cost_value
                    total_aro_cost += aro_cost_value
                    total_cost += total_cost_value
                    total_ale += total_ale_impact_value
                    total_aro_rate += mitigating_control.aro_mitigation_rate
                    mitigating_controls.append({
                        'entry_company_control_id': mitigating_control.id,
                        'company_id': company.id,
                        'company_name': company_control.name,
                        'control_name': control.name,
                        'vendor_name': vendor.name,
                        'max_loss': company.fixed_max_loss,
                        'sle_mitigation_rate': mitigating_control.sle_mitigation_rate,
                        'sle_rate': mitigating_control.sle_mitigation_rate,
                        'sle_rate_display': str(mitigating_control.sle_mitigation_rate) + '%',
                        'aro_mitigation_rate': mitigating_control.aro_mitigation_rate,
                        'aro_rate': mitigating_control.aro_mitigation_rate,
                        'aro_rate_display': str(mitigating_control.aro_mitigation_rate) + '%',
                        'sle_cost_value': sle_cost_value,
                        'sle_cost': '$' + str(sle_cost_value),
                        'aro_cost_value': aro_cost_value,
                        'aro_cost': '$' + str(aro_cost_value),
                        'total_cost_value': total_cost_value,
                        'total_cost': '$' + str(total_cost_value),
                        'total_ale_impact_value': total_ale_impact_value,
                        'total_ale_impact': '$' + str(total_ale_impact_value),
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
                        'total_ale': total_ale
                    }
                })
            except:
                pass
        except:
            pass

    return JsonResponse(rv)
