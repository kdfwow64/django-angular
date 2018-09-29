from django.contrib import admin
from risk.models.entry import EntryActor, EntryCompanyAsset, EntryActorIntent, EntryCompanyControl, EntryActorMotive, EntryCompliance, EntryEventType, EntryCompanyControlFunction, EntryCompanyControlMeasure, EntryCompanyLocation, EntryCompanyControlDependency, EntryResponseResult, EntryRiskType
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


class EntryCompanyControlFunctionInline(admin.TabularInline):

    model = EntryCompanyControlFunction
    extra = 1


class EntryCompanyControlMeasureInline(admin.TabularInline):

    model = EntryCompanyControlMeasure
    extra = 1


class EntryCompanyControlDependencyInline(admin.TabularInline):

    model = EntryCompanyControlDependency
    extra = 1


class EntryCompanyLocationInline(admin.TabularInline):

    model = EntryCompanyLocation
    extra = 1


class EntryResponseResultInline(admin.TabularInline):

    model = EntryResponseResult
    extra = 1


class RegisterAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'deleted_by',
        'company',
    )
    list_filter = (
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'deleted_by',
        'company',
    )
    search_fields = ('name',)


class EntryAdmin(admin.ModelAdmin):

    inlines = (EntryActorInline, EntryCompanyAssetInline,
               EntryCompanyControlInline, EntryComplianceInline, EntryEventTypeInline, EntryCompanyLocationInline, EntryRiskTypeInline)
    list_display = (
        'id',
        'summary',
        'desc',
        'assumption',
        'entry_number',
        'date_created',
        'date_modified',
        'date_deactivated',
        'frequency_multiplier',
        'frequency_notes',
        'impact_notes',
        'additional_mitigation',
        'defined1',
        'defined2',
        'incident_response',
        'created_by',
        'modified_by',
        'entry_owner',
        'register',
        'response',
    )
    list_filter = (
        'date_created',
        'date_modified',
        'date_deactivated',
        'incident_response',
        'created_by',
        'modified_by',
        'entry_owner',
        'register',
        'response',
    )
    search_fields = (
        'summary',
        'desc',
        'assumption',
        'frequency_notes',
        'impact_notes',
        'additional_mitigation',
    )


class EntryTaskAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'summary',
        'desc',
        'due_date',
        'internal_ticket',
        'date_created',
        'date_completed',
        'date_acknowledged',
        'task_owner',
        'created_by',
        'closed_by',
        'deleted_by',
        'task_status',
        'entry',
    )
    list_filter = (
        'due_date',
        'task_owner',
        'created_by',
        'closed_by',
        'deleted_by',
        'task_status',
        'entry',
    )


class EntryActorAdmin(admin.ModelAdmin):

    inlines = (EntryActorIntentInline, EntryActorMotiveInline,)
    list_display = (
        'id_entry',
        'id_actor',
        'detail',
        'is_active',
    )
    list_filter = ('id_entry',)
    search_fields = ('id_entry', 'detail')


class RiskTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'keywords',
        'account',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class EntryCauseAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'keywords',
        'entry',
    )
    list_filter = ('entry',)
    search_fields = ('name',)


class EntryCompanyControlAdmin(admin.ModelAdmin):
    inlines = (EntryCompanyControlFunctionInline,
               EntryCompanyControlMeasureInline, EntryCompanyControlDependencyInline,)
    list_display = ('id',
                    'id_companycontrol',
                    'id_entry',
                    'mitigation_rate',
                    'notes',
                    'url',
                    )
    list_filter = ('id_companycontrol', 'id_entry')


class EntryComplianceAdmin(admin.ModelAdmin):

    list_display = ('id', 'id_compliance', 'id_entry')
    list_filter = ('id_compliance', 'id_entry')


class EntryDependencyEffortAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'percent',
        'notes',
        'dependency_effort',
        'entry_control_dependency',
    )
    list_filter = ('dependency_effort', 'entry_control_dependency')


class EntryEvaluationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'update',
        'date_created',
        'date_evaluated',
        'entry',
        'mitigation_adequacy',
        'user',
    )
    list_filter = ('date_created', 'date_evaluated',
                   'entry', 'mitigation_adequacy', 'user')


class EntryImpactAdmin(admin.ModelAdmin):

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

    list_display = (
        'id',
        'name',
        'desc',
        'notes',
        'entry',
    )
    search_fields = ('name',)


class EntryCompanyLocationAdmin(admin.ModelAdmin):

    list_display = ('id', 'id_entry', 'id_companylocation')
    list_filter = ('id_entry', 'id_companylocation')


class EntryResponseAdmin(admin.ModelAdmin):
    inlines = (EntryResponseResultInline,)
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

    list_display = (
        'id',
        'name',
        'desc',
        'sort_order',
    )
    search_fields = ('name',)


class ResponseAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'sort_order',
        'keywords',
    )
    search_fields = ('name',)


class EntryUrlAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'notes',
        'url',
        'is_internal',
        'is_active',
        'is_recommended',
        'entry')
    list_filter = ('entry',)
    search_fields = ('name',)


class MitigationAdequacyAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'keywords',
    )
    search_fields = ('name',)
