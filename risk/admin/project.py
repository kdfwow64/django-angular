from django.contrib import admin
from risk.models.project import ProjectEntryMap
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ProjectEntryMapInline(admin.TabularInline):

    model = ProjectEntryMap
    extra = 1


class ProjectAdmin(admin.ModelAdmin):

    inlines = (ProjectEntryMapInline,)
    list_display = (
        'id',
        'is_active',
        'name',
        'executive_summary',
        'date_created',
        'date_modified',
        'date_start',
        'date_close',
        'was_cancelled',
        'reason_cancelled',
        'company',
        'organizer',
    )
    list_filter = (
        'is_active',
        'date_created',
        'date_modified',
        'date_start',
        'date_close',
        'was_cancelled',
        'company',
        'organizer',
    )
    search_fields = ('name',)


class ProjectAssumptionAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'summary',
        'detail',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )

    list_filter = (
        'is_active',
        'summary',
        'detail',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )
    search_fields = ('summary',)


class ProjectSuccessCriteriaAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'summary',
        'detail',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )

    list_filter = (
        'is_active',
        'summary',
        'detail',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )
    search_fields = ('summary',)


class ProjectBenefitAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'summary',
        'detail',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )

    list_filter = (
        'is_active',
        'summary',
        'detail',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )
    search_fields = ('summary',)


class ProjectMilestoneAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'summary',
        'detail',
        'date_start',
        'date_complete',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )

    list_filter = (
        'is_active',
        'summary',
        'detail',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )
    search_fields = ('summary',)


class ProjectRiskAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'summary',
        'detail',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'risk_type',
        'project',
    )

    list_filter = (
        'is_active',
        'summary',
        'detail',
        'created_by',
        'modified_by',
        'deactivated_by',
        'risk_type',
        'project',
    )
    search_fields = ('summary', 'risk_type',)


class ProjectRiskTypeAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'name',
        'description',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'account',
    )

    list_filter = (
        'is_active',
        'name',
        'description',
        'created_by',
        'modified_by',
        'deactivated_by',
        'account',
    )
    search_fields = ('name',)


class ProjectBudgetChangeAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'amount',
        'is_increase',
        'reason',
        'is_capex',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'risk_type',
        'project',
    )

    list_filter = (
        'is_active',
        'amount',
        'is_increase',
        'reason',
        'is_capex',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'risk_type',
        'project',
    )
    search_fields = ('reason',)


class ProjectDateChangeAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'day',
        'is_added',
        'reason',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'risk_type',
        'project',
    )

    list_filter = (
        'is_active',
        'day',
        'is_added',
        'reason',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'risk_type',
        'project',
    )
    search_fields = ('reason',)


class ProjectUATAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'summary',
        'detail',
        'result',
        'is_acceptable',
        'date_start',
        'date_complete',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )

    list_filter = (
        'is_active',
        'summary',
        'detail',
        'result',
        'is_acceptable',
        'created_by',
        'modified_by',
        'deactivated_by',
        'project',
    )
    search_fields = ('summary',)


class ProjectUpdateAdmin(admin.ModelAdmin):

    list_display = (
        'is_active',
        'summary',
        'description',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'indicator',
        'project',
    )

    list_filter = (
        'is_active',
        'summary',
        'description',
        'created_by',
        'modified_by',
        'deactivated_by',
        'indicator',
        'project',
    )
    search_fields = ('summary', 'indicator',)
