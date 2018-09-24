"""Home page aka Index page."""
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.conf import settings

from .entry import *
from .company import *
from .compliance import *
from .auth import *
from .actor import *
from .scenario import *

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
        # Fetch to know if the user has access to core account, if yes, just ignore what is fetched.
        # _ = user.accountmembership_set.filter(id_account_id__name=settings.CORE_ACCOUNT, is_company_viewable=1).get()
        _ = user.accountmembership_set.filter(
            id_account_id__name=settings.CORE_ACCOUNT).get()
        # Can see everything
        companies = [{'id': c.id, 'name': c.name} for c in Company.objects.filter(
            Q(is_active=True)).order_by('name').all()]
    except:
        company_dict = {c.id_company.id: c.id_company.name for c in user.companymember_set.filter(
            Q(is_active=True)).all()}
        try:
            # admin_account_membership = user.accountmembership_set.filter(is_admin=1, is_company_viewable=1).all()
            admin_account_membership = user.accountmembership_set.filter(
                is_admin=1).all()
            companies = []
            for account_membership in admin_account_membership:
                company_dict.update({c.id: c.name for c in account_membership.id_account.account_company.filter(
                    Q(is_active=True)).all() if c.id not in company_dict})
        except:
            pass
        companies = [{'id': key, 'name': company_dict[key]} for key in sorted(
            company_dict, key=company_dict.get, reverse=False)]
    return render(request, 'dashboard/subtemplate/sidebar.html', context={'companies': companies})


@login_required
def update_company(request):
    """Sub template for dashboard."""
    try:
        payload = json.loads(request.body.decode('utf8'))
        company_id = payload.get('company_id')
        user = request.user
        company_member = user.companymember_set.filter(
            Q(is_active=True), Q(id_company_id=company_id)).first()
        company_dict = {}
        admin_account_membership = user.accountmembership_set.filter(
            is_admin=1).all()
        for account_membership in admin_account_membership:
            company_dict.update({c.id: c.name for c in account_membership.id_account.account_company.filter(
                Q(is_active=True)).all() if c.id not in company_dict})

        if company_member or company_id in company_dict or user.email == settings.CORE_USER:
            user_profile = request.user.get_profile()
            user_profile.current_company_id = company_id
            user_profile.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure'})

    except:
        return JsonResponse({'status': 'failure'})


@login_required
def template(request, name):
    """Sub template for dashboard."""
    return render(request, 'dashboard/subtemplate/{name}.html'.format(name=name))


@login_required
def views(request, name):
    """HTML views for dashboard."""
    return render(request, 'dashboard/views/{name}.html'.format(name=name))
