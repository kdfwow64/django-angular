"""All views related to Compliance in models/compliance.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    Compliance,
    ComplianceType,
    ComplianceRequirement,
    ComplianceVersion,
)


@login_required
def get_all_compliances_for_dropdown(request):
    """Get all compliances for dropdown."""
    data = []
    for compliance in Compliance.objects.order_by('id').all():
        try:
            type_obj = ComplianceType.objects.get(
                pk=compliance.compliance_type_id)
            type = type_obj.name
        except:
            type = ''
        details = compliance.description
        data.append({'id': compliance.id, 'name': compliance.abbrv, 'type': type,
                     'version': compliance.version_number, 'details': details})

    return JsonResponse(data, safe=False)


@login_required
def get_compliances_with_type(request, type_id):
    """Get all compliances with type."""
    data = []
    try:
        compliances = Compliance.objects.filter(
            compliance_type_id=int(type_id))
    except:
        compliances = []
    for compliance in compliances:
        data.append({'id': compliance.id, 'name': compliance.abbrv,
                     'type_id': compliance.compliance_type_id, 'version': compliance.version_number})

    return JsonResponse(data, safe=False)


@login_required
def get_compliance_requirements_with_name(request, compliance_id):
    """Get all compliance requirements with name."""
    data = []
    try:
        requirements = ComplianceRequirement.objects.filter(
            compliance_id=int(compliance_id))
    except:
        requirements = []
    for requirement in requirements:
        data.append({'id': requirement.id,
                     'detail': requirement.requirement, 'cid': requirement.cid})

    return JsonResponse(data, safe=False)


@login_required
def get_compliance_version_number(request, compliance_id):
    """Get all compliance version with compliance id."""
    try:
        version = ComplianceVersion.objects.get(
            compliance_id=int(compliance_id))
    except:
        version = []
    if version == []:
        data = []
    else:
        data = ({'version_id': version.id,
                 'version_number': version.version_number})

    return JsonResponse(data, safe=False)
