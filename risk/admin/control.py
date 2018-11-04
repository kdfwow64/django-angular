from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
# , ControlCategoryCategory
from risk.models.control import ControlCategoryOperation, ControlCategoryFunction, ControlCategoryControl
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ControlCategoryOperationInline(admin.TabularInline):

    model = ControlCategoryOperation
    extra = 1
    fields = ('id_controloperation',
              'is_active', 'is_deleted', 'created_by')


class ControlCategoryFunctionInline(admin.TabularInline):

    model = ControlCategoryFunction
    extra = 1
    fields = ('id_controlfunction',
              'is_active', 'is_deleted', 'created_by')


class ControlCategoryControlInline(admin.TabularInline):

    model = ControlCategoryControl
    extra = 1
    fields = ('id_controlcategory',
              'is_active', 'is_deleted', 'created_by')


class ControlAdmin(admin.ModelAdmin):

    readonly_fields = ('date_created', 'created_by', 'date_modified', 'modified_by',
                       'date_deleted', 'deleted_by', 'date_deactivated', 'deactivated_by',
                       )
    # radio_fields = {'contact_type': admin.HORIZONTAL}
    autocomplete_fields = ['vendor', ]
    fieldsets = (
        ('Control Specific', {
         'fields': ('name', 'model_number', 'abbrv', 'description', 'vendor',)}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('company', ('is_active', 'is_deleted',), ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_deleted', 'deleted_by',), ('date_deactivated', 'deactivated_by',))}),
    )
    list_select_related = []
    inlines = (ControlCategoryControlInline,)
    list_display = (
        'id',
        'name',
        'model_number',
        'description',
        'abbrv',
        'is_active',
        'vendor',
        'company',
    )
    search_fields = ('name', 'model_number', 'abbrv', 'description')
    list_filter = ('name', 'vendor', 'company')


class ControlCscAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'version', 'number',
                    'description', 'control_csc_family')
    list_filter = ('control_csc_family',)


class ControlCscFamilyAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class ControlDomainAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class ControlFunctionAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class ControlOperationAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
    )
    search_fields = ('name',)


class ControlCategoryAdmin(admin.ModelAdmin):

    inlines = (ControlCategoryOperationInline, ControlCategoryFunctionInline)
    list_select_related = []
    list_display = (
        'name',
        'description',
        'abbrv',
        'keywords',
        'control_category_type',
    )
    list_filter = (
        'date_created',
        'control_category_type',
    )
    search_fields = ('name',)


class ControlCategoryTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'abbrv',
        'keywords',
    )
    search_fields = ('name',)


class DependencyEffortAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
    )
    search_fields = ('name',)
