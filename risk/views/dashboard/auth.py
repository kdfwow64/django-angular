"""All views related to User in models/auth.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    User,
)


@login_required
def get_all_users_for_dropdown(request):
    """Get all compliances for dropdown."""
    data = {}
    # for rt in User.objects.filter().all():
    for rt in User.objects.filter().all():
        data.update({rt.id: rt.full_name})

    return JsonResponse(data)

