"""All views related to Entry in models/entry.py."""
# import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    RiskType,
    Response,
)


@login_required
def api_list_entreis(request):
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


@login_required
def get_all_risk_type_for_dropdown(request):
    """Get all risk types for dropdown."""
    data = {}
    # for rt in RiskType.objects.filter().all():
    for rt in RiskType.objects.filter().all():
        data.update({rt.id: rt.name})

    return JsonResponse(data)


@login_required
def get_all_response_type_for_dropdown(request):
    """Get all respose types for dropdown."""
    data = {}
    for rt in Response.objects.filter().all():
        data.update({rt.id: rt.name})

    return JsonResponse(data)
