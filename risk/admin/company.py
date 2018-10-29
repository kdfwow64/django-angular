from django.contrib import admin
from risk.models.company import (
    CompanyMember,
    CompanyProfile,
    CompanyMemberGrant,
    CompanyControlLocation,
    CompanyTeamMember,
    CompanyAssetSegment,
    CompanyAssetLocation,
    CompanyControlFinding,
    CompanyControlSegment,
    CompanyControlContactCost,
    CompanyControlVendorCost,
    CompanyControlContactProcess,
    CompanyControlVendorProcess,
    CompanyControlTeamProcess,
    CompanyObjectiveRiskType,
    CompanyPlaybookMember
)
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
    fields = ('id_user', 'is_active', 'is_deleted', 'created_by')


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


class CompanyControlContactCostInline(admin.TabularInline):

    model = CompanyControlContactCost
    extra = 1


class CompanyControlVendorCostInline(admin.TabularInline):

    model = CompanyControlVendorCost
    extra = 1


class CompanyControlContactProcessInline(admin.TabularInline):

    model = CompanyControlContactProcess
    extra = 1


class CompanyControlVendorProcessInline(admin.TabularInline):

    model = CompanyControlVendorProcess
    extra = 1


class CompanyControlTeamProcessInline(admin.TabularInline):

    model = CompanyControlTeamProcess
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
    list_select_related = []
    list_display = (
        'id',
        'name',
        'account',
        'is_active',
        'is_deleted',
    )
    list_filter = (
        'is_active',
        'account',
    )
    raw_id_fields = ('naics',)
    search_fields = ('name',)
    ordering = ('name',)


class CompanyMemberAdmin(admin.ModelAdmin):
    inlines = (CompanyMemberGrantInline,)
    readonly_fields = ('id_company', 'id_user')
    list_select_related = []
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


class CompanyMemberRoleAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'company_member_role_type',
        'company',
    )
    list_filter = (
        'company_member_role_type',
        'is_active',
        'company',
    )
    search_fields = ('name',)


class CompanyMemberRoleTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'company',
    )
    list_filter = (
        'is_active',
        'company',
    )
    search_fields = ('name',)


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

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
        'keywords',
        'company',
    )
    search_fields = ('name',)


class CompanyAssetAdmin(admin.ModelAdmin):

    inlines = (CompanyAssetLocationInline, CompanyAssetSegmentInline)
    list_select_related = []
    list_display = (
        'id',
        'name',
        'company',
        'asset_type',
        'asset_owner',
    )
    list_filter = (
        'company',
        'asset_type',
        'asset_owner',
    )
    search_fields = ('name', 'asset_owner')


class CompanyObjectiveAdmin(admin.ModelAdmin):

    inlines = (CompanyObjectiveRiskTypeInline,)
    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'objective_owner',
        'company',
    )
    list_filter = (
        'name',
        'description',
        'is_active',
        'objective_owner',
    )
    search_fields = ('name', 'description', 'objective_owner',)


class CompanyControlAdmin(admin.ModelAdmin):
    inlines = (
        CompanyControlLocationInline,
        CompanyControlSegmentInline,
        CompanyControlContactCostInline,
        CompanyControlVendorCostInline,
        CompanyControlContactProcessInline,
        CompanyControlVendorProcessInline,
        CompanyControlTeamProcessInline,
    )
    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'vendor_control',
        'inline_after',
        'company',
    )
    list_filter = (
        'name',
        'description',
        'vendor_control',
        'company',
    )


class CompanyControlMeasureAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
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

    list_select_related = []
    list_display = (
        'id',
        'measurement',
    )
    list_filter = (
        'measurement',
    )


class CompanyControlOpexAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
    )
    list_filter = (
        'name',
        'description',
        'date_purchased',
        'amount',
        'accounting_id',
    )


class CompanyControlCapexAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'date_purchased',
        'amount',
    )
    list_filter = (
        'name',
        'description',
        'date_purchased',
    )


class CompanyControlDependencyAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'id_companycontrol',
        'id_controldependency',
        'is_active',
        'is_deleted',

    )
    list_filter = (
        'id_companycontrol',
        'id_controldependency',
        'has_contingency',
    )


class CompanyControlCostAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'company_control',
        'amount_paid',
        'cost_type',
        'expenditure',
        'notes',
        'date_paid',
        'is_active',
    )
    list_filter = (
        'company_control',
        'is_active',
        'cost_type',
        'expenditure',
    )
    search_fields = ('notes',)


class CompanyControlCostTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'name',
        'description',
        'is_active',
    )
    list_filter = (
        'name',
        'is_active',
    )
    search_fields = ('name',)


class CompanyContactAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'first_name',
        'last_name',
        'title',
        'main_poc',
        'decision_maker',
        'description',
        'email',
        'company',
        'contact_type',
        'vendor',
    )
    list_filter = (
        'main_poc',
        'decision_maker',
        'is_active',
        'company',
        'contact_type',
        'vendor',
    )


class ContactTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class CompanyTeamAdmin(admin.ModelAdmin):

    inlines = (CompanyTeamMemberInline,)
    list_select_related = []
    list_display = ('id', 'name', 'description', 'abbrv',
                    'company', 'lead', 'is_active')
    list_filter = ('company', 'lead', 'is_active')
    search_fields = ('name',)


class CompanyLocationAdmin(admin.ModelAdmin):

    list_select_related = []
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
    list_select_related = []
    list_display = (
        'id',
        'description',
        'date_start',
        'date_stop',
        'effective_impact',
        'owner',
    )
    list_filter = (
        'date_start',
        'date_stop',
        'owner',
    )


class CompanyPlaybookAdmin(admin.ModelAdmin):

    inlines = (CompanyPlaybookMemberInline,)
    list_select_related = []
    list_display = (
        'name',
        'description',
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

    list_select_related = []
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
