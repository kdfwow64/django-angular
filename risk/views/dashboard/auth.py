"""All views related to User in models/auth.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def get_all_users_for_dropdown(request):
    """Get all compliances for dropdown."""
    user = request.user
    company = user.get_current_company()
    data = [{'id': user.id, 'name': user.full_name}]
    for user in company.user_member.order_by('full_name').all():
        data.append({'id': user.id, 'name': user.full_name})
    return JsonResponse(data, safe=False)
