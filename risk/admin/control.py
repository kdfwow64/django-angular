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
        'account',
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
        'example_title1',
        'example_title2',
        'example_content1',
        'example_content2',
        'control_category_type',
        'account',
    )
    list_filter = (
        'date_created',
        'control_category_type',
        'account',
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
        'sort_order',
    )
    search_fields = ('name',)


class DependencyTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'dependent',
        'keywords',
    )
    list_filter = (
        'dependent',
    )
    search_fields = ('name',)
