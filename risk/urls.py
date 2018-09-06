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

    re_path(r'^dashboard/api/risk-entries/$', dashboard.api_list_risk_entreis, name="api-list-risk-entries"),
    re_path(r'^dashboard/api/risk-entry/create/$', dashboard.CreateRiskEntry.as_view(), name="api-create-risk-entries"),
    re_path(r'^dashboard/api/risk-entry/threat-details/(?P<entry_id>[0-9]+)/$', dashboard.api_update_threat_details, name="api-update-threat-details"),
    re_path(r'^dashboard/api/risk-entry/affected-assets/(?P<entry_id>[0-9]+)/$', dashboard.api_update_affected_assets, name="api-update-affected-assets"),
    re_path(r'^dashboard/api/risk-entry/mitigating-controls/(?P<entry_id>[0-9]+)/$', dashboard.api_update_mitigating_controls, name="api-update-mitigating-controls"),
    re_path(r'^dashboard/api/risk-entry/measurements/(?P<entry_id>[0-9]+)/$', dashboard.api_update_measurements, name="api-update-measurements"),

    re_path(r'^dashboard/api/risk-types/$', dashboard.get_all_risk_type_for_dropdown, name="risk-types-dropdown-list"),
    re_path(r'^dashboard/api/response-types/$', dashboard.get_all_risk_type_for_dropdown, name="response-types-dropdown-list"),
    re_path(r'^dashboard/api/company-assets/$', dashboard.get_all_company_assets_for_dropdown, name="company-assets-dropdown-list"),
    re_path(r'^dashboard/api/company-controls/$', dashboard.get_all_company_control_for_dropdown, name="company-control-dropdown-list"),
    # re_path(r'^dashboard/api/entry-company-controls/$', dashboard.get_all_entry_company_control_for_dropdown, name="entry-company-control-dropdown-list"),
    re_path(r'^dashboard/api/company-control-measures/$', dashboard.get_all_company_control_measures_for_dropdown, name="company-control-measures-dropdown-list"),
    re_path(r'^dashboard/api/company-locations/$', dashboard.get_all_company_locations_for_dropdown, name="company-locations-dropdown-list"),
    re_path(r'^dashboard/api/compliances/$', dashboard.get_all_compliances_for_dropdown, name="compliance-dropdown-list"),
    re_path(r'^dashboard/api/users/$', dashboard.get_all_users_for_dropdown, name="users-dropdown-list"),
    re_path(r'^dashboard/api/actors/$', dashboard.get_all_actors_for_dropdown, name="actors-dropdown-list"),
    re_path(r'^dashboard/api/actor-intents/$', dashboard.get_all_actor_intents_for_dropdown, name="actor-intents-dropdown-list"),
    re_path(r'^dashboard/api/actor-motives/$', dashboard.get_all_actor_motives_for_dropdown, name="actor-motives-dropdown-list"),

    # SHOULD BE THE LAST IN THIS LIST
    re_path(r'^$', home.index, name='index'),
]
