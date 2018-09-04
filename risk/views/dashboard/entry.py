"""Home page aka Index page."""
# import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from django.shortcuts import render
# from django.db.models import Q
# from django.conf import settings

# from risk.models import (
#     Entry
# )


@login_required
def api_list_entreis(request):
    """Index for dashboard."""
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
