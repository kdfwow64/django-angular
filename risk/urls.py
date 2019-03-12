"""URLs for risk app."""
from django.urls import include, re_path
from .views import home, auth, dashboard


urlpatterns = [
    re_path(r'^auth/signin/$', auth.signin, name='auth_signin'),
    re_path(r'^auth/signout/$', auth.signout, name='auth_signout'),
    re_path(r'^auth/register/$', auth.register, name='auth_register'),
    re_path(r'^dashboard/$', dashboard.index, name='dashboard'),
    re_path(r'^dashboard/update-company/$', dashboard.update_company,
            name='dashboard_update_company'),
    re_path(r'^dashboard/template/sidebar.html$', dashboard.sidebar),
    re_path(r'^dashboard/template/(?P<name>[^/]+).html$', dashboard.template),
    re_path(r'^dashboard/views/(?P<name>[^/]+).html$', dashboard.views),

    re_path(r'^dashboard/api/risk-entries/$',
            dashboard.api_list_risk_entries, name="api-list-risk-entries"),
    re_path(r'^dashboard/api/risk-entry/(?P<entry_id>[0-9]+)/$',
            dashboard.api_get_risk_entry, name="api-get-risk-entry"),
    re_path(r'^dashboard/api/risk-entry/create/$',
            dashboard.CreateRiskEntry.as_view(), name="api-create-risk-entries"),
    re_path(r'^dashboard/api/risk-entry/threat-details/(?P<entry_id>[0-9]+)/$',
            dashboard.api_update_threat_details, name="api-update-threat-details"),
    re_path(r'^dashboard/api/risk-entry/affected-assets/(?P<entry_id>[0-9]+)/$',
            dashboard.api_update_affected_assets, name="api-update-affected-assets"),
    re_path(r'^dashboard/api/risk-entry/mitigating-controls/(?P<entry_id>[0-9]+)/$',
            dashboard.api_update_mitigating_controls, name="api-update-mitigating-controls"),
    re_path(r'^dashboard/api/risk-entry/measurements/(?P<entry_id>[0-9]+)/$',
            dashboard.api_update_measurements, name="api-update-measurements"),

    re_path(r'^dashboard/api/risk-types/$',
            dashboard.get_all_risk_type_for_dropdown, name="risk-types-dropdown-list"),
    re_path(r'^dashboard/api/responses/$',
            dashboard.get_all_responses_for_dropdown, name="responses-dropdown-list"),
    re_path(r'^dashboard/api/company-assets/$',
            dashboard.get_all_company_assets_for_dropdown, name="company-assets-dropdown-list"),
    re_path(r'^dashboard/api/company-controls/$',
            dashboard.get_all_company_control_for_dropdown, name="company-control-dropdown-list"),
    # re_path(r'^dashboard/api/entry-company-controls/$', dashboard.get_all_entry_company_control_for_dropdown, name="entry-company-control-dropdown-list"),
    re_path(r'^dashboard/api/company-control-measures/$',
            dashboard.get_all_company_control_measures_for_dropdown, name="company-control-measures-dropdown-list"),
    re_path(r'^dashboard/api/company-locations/$',
            dashboard.get_all_company_locations_for_dropdown, name="company-locations-dropdown-list"),
    re_path(r'^dashboard/api/compliances/$',
            dashboard.get_all_compliances_for_dropdown, name="compliance-dropdown-list"),
    re_path(r'^dashboard/api/users/$',
            dashboard.get_all_users_for_dropdown, name="users-dropdown-list"),
    re_path(r'^dashboard/api/actors/$',
            dashboard.get_all_actors_for_dropdown, name="actors-dropdown-list"),
    re_path(r'^dashboard/api/actor-intents/$',
            dashboard.get_all_actor_intents_for_dropdown, name="actor-intents-dropdown-list"),
    re_path(r'^dashboard/api/actor-motives/$',
            dashboard.get_all_actor_motives_for_dropdown, name="actor-motives-dropdown-list"),
    re_path(r'^dashboard/api/impact-types/$',
            dashboard.get_all_impact_types_for_dropdown, name="impact-type-dropdown-list"),
    re_path(r'^dashboard/api/severity/$',
            dashboard.get_all_severities_for_dropdown,
            name="severity-dropdown-list"),
    re_path(r'^dashboard/api/time-units/$',
            dashboard.get_all_time_units_for_dropdown, name="time-units-dropdown-list"),
    re_path(r'^dashboard/api/frequencies/$',
            dashboard.get_all_frequencies_for_dropdown, name="frequencies-dropdown-list"),
    re_path(r'^dashboard/api/entry-urls/$',
            dashboard.get_all_entry_urls_for_dropdown, name="entry-urls-dropdown-list"),
    re_path(r'^dashboard/api/compliance-types/$',
            dashboard.get_all_compliance_types_for_dropdown, name="compliance-types-dropdown-list"),
    re_path(r'^dashboard/api/compliances-with-type/(?P<type_id>[0-9]+)/$',
            dashboard.get_compliances_with_type, name="compliance-with-type-dropdown-list"),
    re_path(r'^dashboard/api/compliance-requirements-with-name/(?P<compliance_id>[^/]+)/$',
            dashboard.get_compliance_requirements_with_name, name="compliance-requirements-with-name-dropdown-list"),
    re_path(r'^dashboard/api/compliance-version-number/(?P<compliance_id>[0-9]+)/$',
            dashboard.get_compliance_version_number, name="compliance-version-number-dropdown-list"),
    re_path(r'^dashboard/api/get-company-asset/(?P<company_asset_id>[0-9]+)/$',
            dashboard.get_company_asset, name="company-asset-dropdown-list"),
    re_path(r'^dashboard/api/control-details-with-company/(?P<company_id>[0-9]+)/$',
            dashboard.get_control_details_with_company, name="control-details-with-company-type-dropdown-list"),
    re_path(r'^dashboard/api/impact-categories/$',
            dashboard.get_all_impact_categories, name="impact-categories-dropdown-list"),
    re_path(r'^dashboard/api/severity-categories/$',
            dashboard.get_all_severity_categories, name="severity-categories-dropdown-list"),
    re_path(r'^dashboard/api/list-entries-info/$',
            dashboard.api_list_entries_info, name="api-list-entries-info"),
    re_path(r'^dashboard/api/save-file/(?P<count>[0-9]+)/(?P<entry_id>[0-9]+)/(?P<company_id>[0-9]+)/$',
            dashboard.simple_upload, name="api-save-file-entries"),

    # SHOULD BE THE LAST IN THIS LIST
    re_path(r'^$', home.index, name='index'),
]
