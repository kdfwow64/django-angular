"""Home page aka Index page."""
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.conf import settings

from risk.models import (
    # AccountMembership,
    Company,
    # CompanyMember
)
# Create your views here.

@login_required
def index(request):
    """Index for dashboard."""
    return render(request, 'dashboard/index.html')


@login_required
def sidebar(request):
    """Sub template for dashboard sidebar."""
    user = request.user
    try:
        core_account = user.accountmembership_set.filter(id_account_id__name=settings.CORE_ACCOUNT, is_company_viewable=1).get()
        # Can see everything
        companies = [{'id': c.id, 'name': c.name} for c in Company.objects.filter(Q(is_active=True)).all()]
    except:
        try:
            admin_account_membership = user.accountmembership_set.filter(is_admin=1, is_company_viewable=1).all()
            companies = []
            for account_membership in admin_account_membership:
                companies += [{'id': c.id, 'name': c.name} for c in account_membership.id_account.account_company.filter(Q(is_active=True)).all()]
        except:
            companies = [{'id': c.id_company.id, 'name': c.id_company.name} for c in request.user.companymember_set.filter(Q(is_active=True)).all()]
    return render(request, 'dashboard/subtemplate/sidebar.html', context={'companies': companies})

@login_required
def update_company(request):
    """Sub template for dashboard."""
    try:
        # payload = json.loads(request.body.decode('utf8'))
        # company_id = payload.get('company_id')
        # company_member = CompanyMember.objects.filter(Q(id_user=request.user) & Q(is_active=True) & Q(is_default=True)).get()
        # company_member.id_company_id = company_id
        # company_member.save()
        return JsonResponse({'status': 'success'})
    except:
        raise
        return JsonResponse({'status': 'failure'})

@login_required
def template(request, name):
    """Sub template for dashboard."""
    return render(request, 'dashboard/subtemplate/{name}.html'.format(name=name))


@login_required
def views(request, name):
    """HTML views for dashboard."""
    return render(request, 'dashboard/views/{name}.html'.format(name=name))

