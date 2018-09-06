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
def api_list_risk_entreis(request):
    """List entries."""
    user = request.user
    company = user.get_current_company()
    company_registers = company.company_register.first()

    rows = []

    total = 0
    # for register in company_registers:
    register_entries = company_registers.entry
    start = int(request.GET.get('start'))
    length = int(request.GET.get('length'))
    search = request.GET.get('search')

    if search:
        register_entries = register_entries.filter(summary__contains=search)

    total = register_entries.count()
    for entry in register_entries.all()[start:start + length]:
        rows.append([
            entry.entry_number,     # Entry number
            entry.severity,         # Severity = (24 ((entryid)-1)) /(maxrevenueloss)
            entry.mitigation_rate,  #
            entry.get_summary(),    #
            "{first_name} {last_name}".format(entry.entry_owner.first_name, entry.entry_owner.last_name),
            entry.date_created.strftime("%m/%d/%Y"),
            entry.date_modified.strftime("%m/%d/%Y"),
            entry.date_created.strftime("%m/%d/%Y"),
            'Edit'
        ])

    data = {
        'data': rows,
        'draw': int(request.GET.get('draw')),
        'recordsTotal': request.GET.get('draw'),
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
        form = self.form_class(data=request_data)

        if form.is_valid():
            risk_entry = form.save(commit=False)
            risk_entry.entry_owner_id = int(request_data.get("entry_owner"))
            risk_entry.save()

            final_response = Response.objects.get(pk=request_data.get("final_response"))
            if final_response:
                EntryResponse.objects.create(entry=risk_entry, final_response=final_response)

            for risk_type_id in request_data.get("risk_types", []):
                risk_type = RiskType.objects.get(pk=risk_type_id)
                if risk_type:
                    EntryRiskType.objects.create(id_entry=risk_entry, id_risktype=risk_type)

            for location_id in request_data.get("locations", []):
                location = CompanyLocation.objects.get(pk=location_id)
                if location:
                    EntryCompanyLocation.objects.create(id_entry=risk_entry, id_companylocation=location)

            for compliances_id in request_data.get("compliances", []):
                compliance = Compliance.objects.get(pk=compliances_id)
                if compliance:
                    EntryCompliance.objects.create(id_entry=risk_entry, id_compliance=compliance)

            rv = {'status': 'success', 'code': 200, 'id': risk_entry.id}
        else:
            rv = {'status': 'error', 'code': 400, 'errors': form.errors}

        return JsonResponse(rv)


@login_required
def api_update_threat_details(request, entry_id):
    """Update threat entry."""
    risk_entry = Entry.objects.get(pk=entry_id)
    request_data = json.loads(request.body.decode('utf-8'))
    if risk_entry and request.method == 'POST':
        actor = Actor.objects.get(pk=request_data.get('actor_name'))
        if actor:
            entry_actor = EntryActor.objects.create(id_entry=risk_entry, id_actor=actor, detail=request_data.get('detail'))
            for intension_id in request_data.get("intensions", []):
                intension = ActorIntent.objects.get(pk=intension_id)
                if intension:
                    EntryActorIntent.objects.create(id_entryactor=entry_actor, id_actorintent=intension)

            for motives_id in request_data.get("motives", []):
                motive = ActorMotive.objects.get(pk=motives_id)
                if motive:
                    EntryActorMotive.objects.create(id_entryactor=entry_actor, id_actormotive=motive)

        else:
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid actor"]}

        rv = {'status': 'success', 'code': 200, 'id': risk_entry.id}
    else:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}

    return JsonResponse(rv)


@login_required
def api_update_affected_assets(request, entry_id):
    """Update threat entry."""
    risk_entry = Entry.objects.get(pk=entry_id)
    request_data = json.loads(request.body.decode('utf-8'))
    if risk_entry and request.method == 'POST':
        asset = CompanyAsset.objects.get(pk=request_data.get('asset_name'))
        if asset:
            EntryCompanyAsset.objects.create(
                id_entry=risk_entry,
                id_companyasset=asset,
                detail=request_data.get('asset_detail'),
                exposure_percentage=request_data.get('exposure_percentage'),
            )
            risk_entry.impact_notes = request_data.get('impact_notes')
            risk_entry.save()
        else:
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid asset"]}

        rv = {'status': 'success', 'code': 200, 'id': risk_entry.id}
    else:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}

    return JsonResponse(rv)


@login_required
def api_update_mitigating_controls(request, entry_id):
    """Update threat entry."""
    risk_entry = Entry.objects.get(pk=entry_id)
    request_data = json.loads(request.body.decode('utf-8'))
    if risk_entry and request.method == 'POST':
        control = CompanyControl.objects.get(pk=request_data.get('control'))
        if control:
            entry_control = EntryCompanyControl.objects.create(
                id_entry=risk_entry,
                id_companycontrol=control,
                mitigation_rate=request_data.get('mitigation_rate'),
                notes=request_data.get('notes'),
                url=request_data.get('url'),
            )
            risk_entry.addtional_mitigation = request_data.get('addtional_mitigation')
            risk_entry.save()
        else:
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid control"]}

        rv = {'status': 'success', 'code': 200, 'id': risk_entry.id, "entry_control": {entry_control.id: entry_control.id_companycontrol.name}}
    else:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}

    return JsonResponse(rv)


@login_required
def api_update_measurements(request, entry_id):
    """Update threat entry."""
    risk_entry = Entry.objects.get(pk=entry_id)
    request_data = json.loads(request.body.decode('utf-8'))
    if risk_entry and request.method == 'POST':
        try:
            control = EntryCompanyControl.objects.get(pk=request_data.get('control'))
            for measurement_id in request_data.get("measurement", []):
                measurement = CompanyControlMeasure.objects.get(pk=measurement_id)
                if measurement:
                    EntryCompanyControlMeasure.objects.create(id_entrycompanycontrol=control, id_companycontrolmeasure=measurement)

        except:
            rv = {'status': 'error', 'code': 400, 'errors': ["Invalid asset"]}

        rv = {
            'status': 'success',
            'code': 200,
            'id': risk_entry.id,
            'entry_date_create': risk_entry.date_created,
            'created_by': risk_entry.created_by.full_name,
            'date_modified': risk_entry.date_modified,
            'modified_by': risk_entry.modified_by.full_name,
            # 'date_evaluation': risk_entry.date_evaluation,
            # 'mitigation_adequacy': risk_entry.mitigation_adequacy,
            # 'company_asset': risk_entry.company_asset,
            # 'company_control': risk_entry.company_control,
        }
    else:
        rv = {'status': 'error', 'code': 400, 'errors': ["Invalid data"]}

    return JsonResponse(rv)


@login_required
def get_all_risk_type_for_dropdown(request):
    """Get all risk types for dropdown."""
    data = {}
    # for risk_type in RiskType.objects.filter().all():
    for risk_type in RiskType.objects.filter().all():
        data.update({risk_type.id: risk_type.name})

    return JsonResponse(data)


@login_required
def get_all_response_type_for_dropdown(request):
    """Get all respose types for dropdown."""
    data = {}
    for response_type in Response.objects.filter().all():
        data.update({response_type.id: response_type.name})

    return JsonResponse(data)


@login_required
def get_all_entry_company_control_for_dropdown(request):
    """Get all entry company control for dropdown."""
    data = {}
    # for measures in EntryCompanyControl.objects.filter().all():
    for measures in EntryCompanyControl.objects.select_related('id_companycontrol').filter().all():
        data.update({measures.id: measures.id_companycontrol.name})

    return JsonResponse(data)

