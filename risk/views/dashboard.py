"""Home page aka Index page."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# Create your views here.


@login_required
def index(request):
    """Index for dashboard."""
    return render(request, 'dashboard/index.html')


@login_required
def template(request, name):
    """Sub template for dashboard."""
    return render(request, 'dashboard/subtemplate/{name}.html'.format(name=name))


@login_required
def views(request, name):
    """HTML views for dashboard."""
    return render(request, 'dashboard/views/{name}.html'.format(name=name))

