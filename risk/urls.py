"""URLs for risk app."""
from django.urls import include, re_path
from .views import home, auth, dashboard


urlpatterns = [
    re_path(r'^auth/signin/$', auth.signin, name='auth_signin'),
    re_path(r'^auth/signout/$', auth.signout, name='auth_signout'),
    re_path(r'^auth/register/$', auth.register, name='auth_register'),
    re_path(r'^dashboard/$', dashboard.index, name='dashboard'),
    re_path(r'^dashboard/update-company/$', dashboard.update_company, name='dashboard_update_company'),
    re_path(r'^dashboard/template/sidebar.html$', dashboard.sidebar),
    re_path(r'^dashboard/template/(?P<name>[^/]+).html$', dashboard.template),
    re_path(r'^dashboard/views/(?P<name>[^/]+).html$', dashboard.views),
    re_path(r'^dashboard/api/entries/$', dashboard.api_list_entreis, name="api-list-entries"),
    re_path(r'^dashboard/api/risk-types/$', dashboard.get_all_risk_type_for_dropdown, name="risk-types-dropdown-list"),
    re_path(r'^dashboard/api/response-types/$', dashboard.get_all_risk_type_for_dropdown, name="response-types-dropdown-list"),
    re_path(r'^dashboard/api/company-locations/$', dashboard.get_all_company_locations_for_dropdown, name="company-locations-dropdown-list"),
    re_path(r'^dashboard/api/compliances/$', dashboard.get_all_compliances_for_dropdown, name="compliance-dropdown-list"),
    re_path(r'^dashboard/api/users/$', dashboard.get_all_users_for_dropdown, name="users-dropdown-list"),

    # SHOULD BE THE LAST IN THIS LIST
    re_path(r'^$', home.index, name='index'),
]
