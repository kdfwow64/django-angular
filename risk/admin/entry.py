from django.contrib import admin
from django.utils.html import format_html
from risk.models.entry import EntryActor, EntryCompanyAsset, EntryActorIntent, EntryCompanyControl, EntryActorMotive, EntryCompliance, EntryEventType, EntryCompanyControlCIATriad, EntryCompanyControlMeasure, EntryCompanyLocation, EntryResponseResult, EntryRiskType, Entry, EntryUrl
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class EntryRiskTypeInline(admin.TabularInline):

    model = EntryRiskType
    extra = 1


class EntryActorInline(admin.TabularInline):

    model = EntryActor
    extra = 1


class EntryActorIntentInline(admin.TabularInline):

    model = EntryActorIntent
    extra = 1


class EntryActorMotiveInline(admin.TabularInline):

    model = EntryActorMotive
    extra = 1


class EntryCompanyAssetInline(admin.TabularInline):

    model = EntryCompanyAsset
    extra = 1


class EntryCompanyControlInline(admin.TabularInline):

    model = EntryCompanyControl
    extra = 1


class EntryComplianceInline(admin.TabularInline):

    model = EntryCompliance
    extra = 1


class EntryEventTypeInline(admin.TabularInline):

    model = EntryEventType
    extra = 1


class EntryCompanyControlCIATriadInline(admin.TabularInline):

    model = EntryCompanyControlCIATriad
    extra = 1


class EntryCompanyControlMeasureInline(admin.TabularInline):

    model = EntryCompanyControlMeasure
    extra = 1


class EntryCompanyLocationInline(admin.TabularInline):

    model = EntryCompanyLocation
    extra = 1


class EntryResponseResultInline(admin.TabularInline):

    model = EntryResponseResult
    extra = 1


class RegisterAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'date_created',
        'created_by',
        'company',
    )
    list_filter = (
        'created_by',
        'company',
    )
    search_fields = ('name',)


class EntryAdmin(admin.ModelAdmin):

    readonly_fields = ('date_created', 'created_by', 'date_modified', 'modified_by',
                       'date_deleted', 'deleted_by', 'date_deactivated', 'deactivated_by',
                       'entry_number', 'register', )
    radio_fields = {'response': admin.HORIZONTAL}
    fieldsets = (
        ('Basic Info', {
         'fields': ('register', 'response', 'entry_number', ('summary', 'description',), 'assumption', 'additional_mitigation',)}),
        ('Threat Scenario', {
         'fields': ('aro_notes', 'impact_notes',)}),
        ('Advanced Options', {
         'fields': ('is_completed', ('evaluation_flg', 'evaluation_days',), 'incident_response',)}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (('is_active', 'is_deleted',), ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_deleted', 'deleted_by',), ('date_deactivated', 'deactivated_by',))}),
    )

    inlines = (EntryActorInline, EntryCompanyAssetInline,
               EntryCompanyControlInline, EntryComplianceInline, EntryEventTypeInline, EntryCompanyLocationInline, EntryRiskTypeInline)
    list_select_related = []
    list_display = (
        'id',
        'register',
        'summary',
        'description',
        'assumption',
        'entry_number',
        'incident_response',
        'response',
        'is_completed',
    )
    list_filter = (
        'entry_owner',
        'register',
        'response',
        'is_completed',
    )
    search_fields = (
        'summary',
        'description',
        'assumption',
        'aro_notes',
        'impact_notes',
        'additional_mitigation',
    )
    ordering = ['register', 'entry_number']


class EntryTaskAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'summary',
        'description',
        'due_date',
        'internal_ticket',
        'date_created',
        'date_completed',
        'date_acknowledged',
        'task_owner',
        'task_status',
        'entry',
    )
    list_filter = (
        'task_owner',
        'task_status',
        'entry',
    )


class EntryActorAdmin(admin.ModelAdmin):

    inlines = (EntryActorIntentInline, EntryActorMotiveInline,)
    list_select_related = []
    list_display = (
        'id_entry',
        'id_actor',
        'detail',
        'is_active',
    )
    list_filter = ('id_entry',)
    search_fields = ('id_entry', 'detail')


class RiskTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
        'company',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class EntryCauseAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
        'entry',
    )
    list_filter = ('entry',)
    search_fields = ('name',)


class EntryCompanyControlAdmin(admin.ModelAdmin):
    inlines = (EntryCompanyControlCIATriadInline,
               EntryCompanyControlMeasureInline,)
    list_display = ('id',
                    'id_companycontrol',
                    'id_entry',
                    'aro_mitigation_rate',
                    'impact_mitigation_rate',
                    'notes',
                    'url',
                    )
    list_filter = ('id_companycontrol', 'id_entry')


class EntryComplianceAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'id_compliance', 'id_entry')
    list_filter = ('id_compliance', 'id_entry')


class EntryDependencyEffortAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'percent',
        'notes',
        'dependency_effort',
        'entry_control_dependency',
    )
    list_filter = ('dependency_effort', 'entry_control_dependency')


class EntryEvaluationAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'update',
        'date_created',
        'date_evaluated',
        'entry',
        'mitigation_adequacy',
        'evaluator',
        'approver',
    )
    list_filter = ('date_created', 'date_evaluated',
                   'entry', 'mitigation_adequacy', 'evaluator', 'approver',)


class EntryImpactAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'fixed_cost',
        'pml_cost',
        'monetary_value_toggle',
        'notes',
        'entry',
        'impact_type',
    )
    list_filter = ('entry', 'impact_type')


class EntryIndicatorAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'notes',
        'entry',
    )
    search_fields = ('name',)


class EntryCompanyLocationAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'id_entry', 'id_companylocation')
    list_filter = ('id_entry', 'id_companylocation')


class EntryResponseSubmissionAdmin(admin.ModelAdmin):
    inlines = (EntryResponseResultInline,)
    list_select_related = []
    list_display = (
        'id',
        'date_presented',
        'date_decision',
        'date_target',
        'justification',
        'budget',
        'notes',
        'entry',
        'suggested_response',
    )
    list_filter = (
        'date_presented',
        'date_decision',
        'entry',
        'suggested_response',
    )


class ResponseVoteAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
    )
    search_fields = ('name',)


class ResponseAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
        'keywords',
    )
    search_fields = ('name',)


class EntryUrlAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'show_entry_url',
        'notes',
        'is_internal',
        'is_active',
        'is_recommended',
        'entry')
    list_filter = ('entry',)
    search_fields = ('name',)

    def show_entry_url(self, obj):
        return format_html("<a href='{url}'>{name}</a>", url=obj.url, name=obj.name)

    show_entry_url.short_description = "Entry URL"


class MitigationAdequacyAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)
