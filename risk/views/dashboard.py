"""Home page aka Index page."""
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from risk.models import Company, CompanyMember

@login_required
def index(request):
    """Index for dashboard."""
    return render(request, 'dashboard/index.html')


@login_required
def sidebar(request):
    """Sub template for dashboard sidebar."""
    companies = [{'id': c.id, 'name': c.name} for c in Company.objects.filter(is_active=True).order_by('name').all()]
    return render(request, 'dashboard/subtemplate/sidebar.html', context={'companies': companies})

@login_required
def update_company(request):
    """Sub template for dashboard."""
    try:
        payload = json.loads(request.body.decode('utf8'))
        company_id = payload.get('company_id')
        company_member = CompanyMember.objects.filter(id_user=request.user).get()
        company_member.id_company_id = company_id
        company_member.save()
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

