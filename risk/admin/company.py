from django.contrib import admin
from risk.models.company import CompanyMember, CompanyProfile, CompanyMemberGrant, CompanyControlLocation, CompanyTeamMember, CompanyAssetSegment, CompanyAssetLocation, CompanyControlFinding, CompanyControlSegment, CompanyControlDependency, CompanyObjectiveRiskType, CompanyPlaybookMember
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class CompanyProfileInline(admin.StackedInline):

    model = CompanyProfile
    can_delete = False
    verbose_name_plural = 'Company Profile'


class CompanyMemberInline(admin.TabularInline):

    model = CompanyMember
    extra = 1


class CompanyMemberGrantInline(admin.TabularInline):

    model = CompanyMemberGrant
    extra = 4


class CompanyAssetSegmentInline(admin.TabularInline):

    model = CompanyAssetSegment
    extra = 1


class CompanyAssetLocationInline(admin.TabularInline):

    model = CompanyAssetLocation
    extra = 1


class CompanyControlSegmentInline(admin.TabularInline):

    model = CompanyControlSegment
    extra = 1


class CompanyControlLocationInline(admin.TabularInline):

    model = CompanyControlLocation
    extra = 1


class CompanyControlDependencyInline(admin.TabularInline):

    model = CompanyControlDependency
    extra = 1


class CompanyTeamMemberInline(admin.TabularInline):

    model = CompanyTeamMember
    extra = 1


class CompanyControlFindingInline(admin.TabularInline):

    model = CompanyControlFinding
    extra = 1


class CompanyObjectiveRiskTypeInline(admin.TabularInline):

    model = CompanyObjectiveRiskType
    extra = 1


class CompanyPlaybookMemberInline(admin.TabularInline):

    model = CompanyPlaybookMember
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    inlines = (CompanyProfileInline, CompanyMemberInline,)
    list_display = (
        'id',
        'name',
        'account',
        'fixed_max_loss',
        'par_max_loss',
        'monetary_value_toggle',
        'annual_revenue',
        'weight_frequency',
        'weight_impact',
        'resilience_max',
        'evaluation_days',
        'evaluation_alert_days',
        'is_active',
        'date_deactivated',
        'date_created',
        'date_modified',
        'date_deleted',
        'utility_field',
        'created_by',
        'modified_by',
        'deactivated_by',
        'deleted_by',
        'account',
        'naics',
        'currencytype',
    )
    list_filter = (
        'monetary_value_toggle',
        'is_active',
        'date_deactivated',
        'date_created',
        'date_modified',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'deleted_by',
        'account',
        'currencytype',
    )
    raw_id_fields = ('naics',)
    search_fields = ('name',)
    ordering = ('name',)


class CompanyMemberAdmin(admin.ModelAdmin):
    inlines = (CompanyMemberGrantInline,)
    readonly_fields = ('id_company', 'id_user')
    list_display = (
        'id_company',
        'id_user',
        'is_active',
    )
    list_filter = (
        'id_user',
        'id_company',
        'is_active',
    )
    search_fields = ('id_user', 'id_company',)
    ordering = ('id_company',)


# class CompanyMemberGrantAdmin(admin.ModelAdmin):
#     list_display = (
#         'id_companymember',
#         'id_usergrant',
#         'is_active',
#     )
#     list_filter = (
#         'id_usergrant',
#         'id_companymember',
#         'is_active',
#     )
#     search_fields = ('id_usergrant', 'id_companymember',)
#     ordering = ('id_companymember',)


class CompanyAssetTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'sort_order',
        'keywords',
        'company',
    )
    search_fields = ('name',)


class CompanyAssetAdmin(admin.ModelAdmin):

    inlines = (CompanyAssetLocationInline, CompanyAssetSegmentInline)
    list_display = (
        'id',
        'name',
        'notes',
        'asset_value_fixed',
        'asset_quantity_fixed',
        'asset_value_par',
        'asset_value_timed',
        'asset_timed_quantity_relative',
        'asset_timed_quantity_avaliable',
        'asset_value_toggle',
        'evaluation_days',
        'evaluation_flg',
        'company',
        'asset_type',
        'asset_owner',
    )
    list_filter = (
        'company',
        'asset_type',
        'asset_owner',
        'asset_value_toggle',
    )
    search_fields = ('name', 'asset_owner')


class CompanyObjectiveAdmin(admin.ModelAdmin):

    inlines = (CompanyObjectiveRiskTypeInline,)
    list_display = (
        'id',
        'name',
        'desc',
        'monetary_value_start',
        'monetary_value_end',
        'monetary_value_current',
        'date_start',
        'date_end',
        'date_created',
        'is_active',
        'objective_owner',
        'company',
    )
    list_filter = (
        'name',
        'desc',
        'is_active',
        'objective_owner',
    )
    search_fields = ('name', 'desc', 'objective_owner',)


class CompanyControlAdmin(admin.ModelAdmin):
    inlines = (CompanyControlLocationInline,
               CompanyControlSegmentInline, CompanyControlDependencyInline)
    list_display = (
        'id',
        'name',
        'desc',
        'abbrv',
        'alias',
        'version',
        'avg_annual_upkeep',
        'recovery_integer',
        'recovery_time_unit',
        'date_maint',
        'centralized',
        'budgeted',
        'evaluation_days',
        'evaluation_flg',
        'defined1_data',
        'date_defined1',
        'defined2_data',
        'date_defined2',
        'is_active',
        'vendor_control',
        'inline_after',
        'company',
    )
    list_filter = (
        'name',
        'desc',
        'vendor_control',
        'is_active',
        'alias',
        'version',
        'avg_annual_upkeep',
        'date_maint',
        'inline_after',
        'centralized',
        'budgeted',
        'company',
    )


class CompanyControlMeasureAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'formula',
        'unit',
        'baseline',
        'target',
        'tolerance',
        'company_control',
    )
    list_filter = (
        'company_control',
    )


class CompanyControlMeasurementResultAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'result',
        'date_created',
        'created_by',
        'measurement',
    )
    list_filter = (
        'measurement',
    )


class CompanyControlOpexAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'detail',
        'date_created',
        'date_purchased',
        'amount',
        'accounting_id',
    )
    list_filter = (
        'detail',
        'date_created',
        'date_purchased',
        'amount',
        'accounting_id',
    )


class CompanyControlCapexAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'detail',
        'date_created',
        'date_purchased',
        'amount',
        'accounting_id',
    )
    list_filter = (
        'detail',
        'date_created',
        'date_purchased',
        'amount',
        'accounting_id',
    )


class CompanyControlDependencyAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'id_companycontrol',
        'id_controldependency',
        'row',
        'is_active',
        'has_contingency',
        'contingency_plan',
        'notes',

    )
    list_filter = (
        'id_companycontrol',
        'id_controldependency',
        'has_contingency',
    )


class CompanyControlCostAdmin(admin.ModelAdmin):

    list_display = (
        'company_control',
        'amount_paid',
        'cost_type',
        'expenditure',
        'notes',
        'date_paid',
        'date_created',
        'is_active',
    )
    list_filter = (
        'company_control',
        'date_paid',
        'is_active',
        'cost_type',
        'expenditure',
    )
    search_fields = ('notes',)


class CompanyControlCostTypeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'desc',
        'is_active',
        'account',
    )
    list_filter = (
        'name',
        'is_active',
        'account',
    )
    search_fields = ('name',)


class CompanyContactAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'first_name',
        'last_name',
        'title',
        'main_poc',
        'decision_maker',
        'desc',
        'email',
        'office_phone',
        'office_phone_ext',
        'cell_phone',
        'notes',
        'is_active',
        'defined1_data',
        'date_defined1',
        'defined2_data',
        'date_defined2',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'reports_to',
        'created_by',
        'modified_by',
        'deactivated_by',
        'deleted_by',
        'company',
        'contact_type',
        'vendor',
    )
    list_filter = (
        'main_poc',
        'decision_maker',
        'is_active',
        'date_defined1',
        'date_defined2',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'reports_to',
        'created_by',
        'modified_by',
        'deactivated_by',
        'deleted_by',
        'company',
        'contact_type',
        'vendor',
    )


class ContactTypeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'desc')
    search_fields = ('name',)


class CompanyTeamAdmin(admin.ModelAdmin):

    inlines = (CompanyTeamMemberInline,)
    list_display = ('id', 'name', 'desc', 'abbrv',
                    'company', 'lead', 'is_active')
    list_filter = ('company', 'lead', 'is_active')
    search_fields = ('name',)


class CompanyLocationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'countrycode',
        'state',
        'city',
        'hq',
        'is_active',
        'geolat',
        'geolon',
        'abbrv',
        'company',
    )
    list_filter = ('hq', 'company', 'is_active')
    search_fields = ('name',)


class CompanyFindingAdmin(admin.ModelAdmin):

    inlines = (CompanyControlFindingInline,)
    list_display = (
        'id',
        'desc',
        'date_created',
        'date_modified',
        'date_start',
        'date_stop',
        'date_deleted',
        'effective_impact',
        'owner',
        'created_by',
        'modified_by',
        'deleted_by',
    )
    list_filter = (
        'date_created',
        'date_modified',
        'date_start',
        'date_stop',
        'date_deleted',
        'owner',
        'created_by',
        'modified_by',
        'deleted_by',
    )


class CompanyPlaybookAdmin(admin.ModelAdmin):

    inlines = (CompanyPlaybookMemberInline,)
    list_display = (
        'name',
        'summary',
        'created_by',
        'modified_by',
        'deactivated_by',
        'playbook_owner',
        'evaluation_days',
        'evaluation_flg',
        'company',
    )
    list_filter = (
        'playbook_owner',
        'evaluation_flg',
        'company',
    )


class CompanyPlaybookActionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'action',
        'sequence_order',
        'attest_days',
        'attest_flg',
        'date_last_attested',
        'action_type',
        'company_playbook',
        'playbook_action_owner',
    )
    list_filter = (
        'attest_flg',
        'action_type',
        'company_playbook',
        'playbook_action_owner',
    )
