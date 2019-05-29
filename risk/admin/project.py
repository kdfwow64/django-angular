from django.contrib import admin
from risk.models.utility import linkify
from risk.models.project import ProjectEntry
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ProjectEntryInline(admin.TabularInline):

    model = ProjectEntry
    extra = 1


class ProjectAdmin(admin.ModelAdmin):

    inlines = (ProjectEntryInline,)
    list_select_related = []
    list_display = (
        'id',
        'is_active',
        'name',
        'description',
        'estimated_days',
        'was_cancelled',
        'reason_cancelled',
        'company',
        'organizer',
    )
    list_filter = (
        'is_active',
        'was_cancelled',
        'company',
        'organizer',
    )
    search_fields = ('name',)


class ProjectAssumptionAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'summary',
        'detail',
        'project',
    )

    list_filter = (
        'is_active',
        'project',
    )
    search_fields = ('summary',)


class ProjectSuccessCriteriaAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'is_deleted',
        'summary',
        'detail',
        'created_by',
        'modified_by',
        'project',
    )

    list_filter = (
        'is_active',
        'project',
    )
    search_fields = ('summary',)


class ProjectBenefitAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'summary',
        'detail',
        'date_created',
        'date_deleted',
        'created_by',
        'project',
    )

    list_filter = (
        'is_active',
        'project',
    )
    search_fields = ('summary',)


class ProjectMilestoneAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'summary',
        'detail',
        'rag',
        'date_start',
        'date_created',
        'created_by',
        'project',
    )

    list_filter = (
        'is_active',
        'project',
        'rag',
    )
    search_fields = ('summary', 'rag',)


class ProjectProgressAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'is_enabled',
        'summary',
        'date_start',
        'date_created',
        'created_by',
        'project',
    )

    list_filter = (
        'is_active',
        'is_enabled',
        'project',
    )
    search_fields = ('summary',)


class ProjectNextStepAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'is_enabled',
        'summary',
        'date_start',
        'date_created',
        'created_by',
        'project',
    )

    list_filter = (
        'is_active',
        'is_enabled',
        'project',
    )
    search_fields = ('summary',)


class ProjectRiskAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'summary',
        'detail',
        'date_created',
        'date_deleted',
        'created_by',
        'risk_type',
        'project',
    )

    list_filter = (
        'is_active',
        'project',
    )
    search_fields = ('summary', 'risk_type',)


class ProjectRiskTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'name',
        'description',
        'date_created',
        'created_by',
        'company',
    )

    list_filter = (
        'is_active',
        'company',
    )
    search_fields = ('name',)


class ProjectBudgetChangeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'amount',
        'is_increase',
        'reason',
        'is_capex',
        'date_created',
        'created_by',
        'risk_type',
        'project',
    )

    list_filter = (
        'is_active',
        'is_increase',
        'project',
    )
    search_fields = ('reason',)


class ProjectDateChangeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'days',
        'is_added',
        'reason',
        'date_created',
        'created_by',
        'risk_type',
        'project',
    )

    list_filter = (
        'is_active',
        'days',
        'is_added',
        'project',
    )
    search_fields = ('reason',)


class ProjectUATAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'summary',
        'detail',
        'result',
        'is_acceptable',
        'date_start',
        'date_complete',
        'date_created',
        'created_by',
        'project',
    )

    list_filter = (
        'is_active',
        'project',
    )
    search_fields = ('summary',)


class ProjectUpdateAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'is_active',
        'summary',
        'description',
        'date_created',
        'created_by',
        'rag',
        'project',
    )

    list_filter = (
        'is_active',
        'rag',
        'project',
    )
    search_fields = ('summary', 'rag',)
