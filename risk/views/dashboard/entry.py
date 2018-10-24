"""All views related to Entry in models/entry.py."""
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.views import View

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
    EntryResponse,
    EntryRiskType,
    Response,
    RiskType,
)
from risk.forms.entry import(
    RiskEntryBasicForm,
)


@login_required
def api_list_risk_entries(request):
    """List entries."""
    user = request.user
    company = user.get_current_company()
    # Get fist register for company from entry.py/Register
    company_register = company.get_active_register()

    rows = []
    total = 0

    register_entries = company_register.entry

    # start = int(request.GET.get('start', '0'))
    # length = int(request.GET.get('length', '10'))
    # search = request.GET.get('search', '')

    # if search:
    #     register_entries = register_entries.filter(summary__contains=search)

    total = register_entries.count()

    for entry in register_entries.order_by('-date_modified').all():

        rows.append({
            'entry_number': entry.entry_number,     # Entry number
            # Severity = (24 ((entryid)-1)) /(maxrevenueloss)
            'severity': entry.severity,
            'mr': entry.mitigation_rate,  #
            'summary': entry.get_summary(),    #
            'owner_name': entry.entry_owner.full_name,
            'created_date': entry.date_created.strftime("%m/%d/%Y"),
            'modified_date': entry.date_modified.strftime("%m/%d/%Y"),
            'evaluated': entry.date_evaluated.strftime("%m/%d/%Y") if entry.date_evaluated else '',
            'id': entry.id,
            'response': entry.has_response,
            'impact': entry.impact,
            'severity_dd': entry.severity,
            'compliance': entry.has_compliance,
            'owner_id': entry.entry_owner.id,
            'active': 1 if entry.is_active else 0,
            'impact_notes': entry.impact_notes,
            'description': entry.description,
        })

    data = {
        'data': rows,
        'draw': int(request.GET.get('draw', 0)),
        'recordsTotal': total,
        'recordsFiltered': len(rows),
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

            risk_entry.entry_owner_id = int(
                request_data.get("entry_owner", request.user.id))
            risk_entry.modified_by = request.user
            risk_entry.save()

            # Select single dropdown
            try:
                final_response = Response.objects.get(
                    pk=request_data.get("final_response"))
                try:
                    entry_response = EntryResponse.objects.filter(
                        entry=risk_entry).latest('id')
                    entry_response.final_response = final_response
                    entry_response.save()
                except:
                    EntryResponse.objects.create(
                        entry=risk_entry, final_response=final_response)
            except:
                pass

            # Select multiple dropdowns - Risk Type
            selected_rt = request_data.get("risk_types", [])
            for ert in risk_entry.entryrisktype.all():
                try:
                    selected_rt.remove(ert.id_risktype_id)
                except:  # This risktype is not selected anymore
                    ert.delete()
            # Add new RiskType
            for risk_type_id in selected_rt:
                try:
                    risk_type = RiskType.objects.get(pk=risk_type_id)
                    EntryRiskType.objects.get_or_create(
                        id_entry=risk_entry, id_risktype=risk_type)
                except:
                    pass

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
            selected_cp = request_data.get("compliances", [])
            for ecp in risk_entry.entrycompliance.all():
                try:
                    selected_cp.remove(ecp.id_compliance_id)
                except:  # This Compliance is not selected anymore
                    ecp.delete()
            # Add new Compliance
            for compliances_id in selected_cp:
                try:
                    compliance = Compliance.objects.get(pk=compliances_id)
                    EntryCompliance.objects.get_or_create(
                        id_entry=risk_entry, id_compliance=compliance)
                except:
                    pass

            rv = {'status': 'success', 'code': 200, 'id': risk_entry.id}
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
                        pk=request_data.get('actor_name'))
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
                    selected_intents = request_data.get("intentions", [])
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
                    selected_motives = request_data.get("motives", [])
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
                        pk=request_data.get('asset_name'))
                    entry_asset_id = request_data.get('entry_asset_id')
                    try:
                        entry_asset = EntryCompanyAsset.objects.get(
                            id=entry_asset_id, id_entry=risk_entry)
                        entry_asset.id_companyasset = asset
                        entry_asset.detail = request_data.get('asset_detail')
                        entry_asset.exposure_factor = request_data.get(
                            'exposure_factor')
                        entry_asset.save()
                    except:
                        EntryCompanyAsset.objects.create(
                            id_entry=risk_entry,
                            id_companyasset=asset,
                            detail=request_data.get('asset_detail'),
                            exposure_factor=request_data.get(
                                'exposure_factor'),
                        )
                except:
                    rv = {'status': 'error', 'code': 400,
                          'errors': ["Invalid asset"]}
            risk_entry.impact_notes = data.get('impact_notes')
            risk_entry.save()

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
            measurement_controls = []
            for request_data in payload:
                try:
                    control = CompanyControl.objects.get(
                        pk=request_data.get('control'))
                    entry_mcontrol_id = request_data.get('entry_mcontrol_id')
                    try:
                        entry_control = EntryCompanyControl.objects.get(
                            id=entry_mcontrol_id, id_entry=risk_entry)
                        entry_control.id_companycontrol = control
                        entry_control.mitigation_rate = request_data.get(
                            'mitigation_rate', 0) or 0
                        entry_control.notes = request_data.get('notes')
                        entry_control.url = request_data.get('url')
                        entry_control.save()
                    except:
                        entry_control = EntryCompanyControl.objects.create(
                            id_entry=risk_entry,
                            id_companycontrol=control,
                            mitigation_rate=request_data.get(
                                'mitigation_rate', 0) or 0,
                            notes=request_data.get('notes'),
                            url=request_data.get('url'),
                        )
                    measurement_controls.append(
                        {'id': entry_control.id, 'name': entry_control.id_companycontrol.name})

                except:
                    rv = {'status': 'error', 'code': 400,
                          'errors': ["Invalid control"]}

            risk_entry.addtional_mitigation = data.get('addtional_mitigation')
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
def get_all_response_type_for_dropdown(request):
    """Get all respose types for dropdown."""
    data = []
    for response_type in Response.objects.order_by('name').all():
        data.append({'id': response_type.id, 'name': response_type.name})
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
            # Get fist register for company from entry.py/Register
            risk_entry = request.user.get_current_company(
            ).get_active_register().entry.get(pk=entry_id)
            try:
                final_response = risk_entry.entryresponse.latest(
                    'id').final_response_id
            except:
                final_response = 1

            rv.update({
                'basicinfo': {
                    'entry_id': risk_entry.id,
                    'summary': risk_entry.summary,
                    'description': risk_entry.description,
                    'risk_types': [ert.id_risktype_id for ert in risk_entry.entryrisktype.all()],
                    'final_response': final_response,
                    'locations': [loc.id_companylocation_id for loc in risk_entry.entry_companylocation.all()] or [1, ],
                    'compliances': [rec.id_compliance_id for rec in risk_entry.entrycompliance.all()],
                    'entry_owner': risk_entry.entry_owner_id or request.user.id,
                    'aro_multiplier': risk_entry.aro_multiplier,
                    'aro_notes': risk_entry.aro_notes,
                }
            })
            try:
                threat_details = []
                for entry_actor in risk_entry.actor_entry.order_by('id').all():
                    threat_details.append({
                        'entry_actor_id': entry_actor.id,
                        'actor_name': entry_actor.id_actor_id,
                        'intentions': [iea.id for iea in entry_actor.intentions.all()],
                        'motives': [iea.id for iea in entry_actor.motives.all()],
                        'detail': entry_actor.detail,
                    })

                rv.update({'threat_details': {'multidata': threat_details}})

            except:
                pass

            try:
                affected_assets = []
                for entry_company_asset in risk_entry.companyasset_entry.order_by('id').all():
                    affected_assets.append({
                        'entry_asset_id': entry_company_asset.id,
                        'asset_name': entry_company_asset.id_companyasset_id,
                        'exposure_factor': entry_company_asset.exposure_factor,
                        'asset_detail': entry_company_asset.detail,
                    })
                rv.update({'affected_assets': {
                          'multidata': affected_assets, 'impact_notes': risk_entry.impact_notes}})
            except:
                pass

            try:
                mitigating_controls = []
                measurements = []
                measurement_controls = []

                for mitigating_control in risk_entry.companycontrol_entry.order_by('id').all():
                    mitigating_controls.append({
                        'entry_mcontrol_id': mitigating_control.id,
                        'control': mitigating_control.id_companycontrol_id,
                        'mitigation_rate': mitigating_control.mitigation_rate,
                        'notes': mitigating_control.notes,
                        'url': mitigating_control.url,
                    })
                    measurements.append({
                        'entry_mcontrol_id': mitigating_control.id,
                        'control': mitigating_control.id_companycontrol_id,
                        'measurement': [ccme.id_companycontrolmeasure_id for ccme in mitigating_control.companycontrolmeasure_entry.all()],
                    })
                    measurement_controls.append(
                        {'id': mitigating_control.id_companycontrol.id, 'name': mitigating_control.id_companycontrol.name})

                rv.update({
                    'mitigating_controls': {'multidata': mitigating_controls, 'addtional_mitigation': risk_entry.addtional_mitigation, },
                    'measurements': {'multidata': measurements},
                    'measurement_controls': measurement_controls,
                })
            except:
                pass
        except:
            pass

    return JsonResponse(rv)
