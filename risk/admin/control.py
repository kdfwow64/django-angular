from django.contrib import admin
from risk.models.control import ControlCategoryOperation, ControlCategoryFunction
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ControlCategoryOperationInline(admin.TabularInline):

    model = ControlCategoryOperation
    extra = 1


class ControlCategoryFunctionInline(admin.TabularInline):

    model = ControlCategoryFunction
    extra = 1


class ControlAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'model_number',
        'description',
        'abbrv',
        'is_active',
        'control_category',
        'vendor',
    )
    search_fields = ('name',)


class ControlCscAdmin(admin.ModelAdmin):

    list_display = ('id', 'version', 'number',
                    'description', 'control_csc_family')
    list_filter = ('control_csc_family',)


class ControlCscFamilyAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class ControlDomainAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class ControlFunctionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class ControlOperationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
    )
    search_fields = ('name',)


class ControlCategoryAdmin(admin.ModelAdmin):

    inlines = (ControlCategoryOperationInline, ControlCategoryFunctionInline)
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

    list_display = (
        'id',
        'name',
        'description',
        'abbrv',
        'keywords',
    )
    search_fields = ('name',)


class DependencyEffortAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
    )
    search_fields = ('name',)


class DependencyTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'dependent',
    )
    list_filter = (
        'dependent',
    )
    search_fields = ('name',)
