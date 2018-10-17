from django.contrib import admin
from risk.models.vendor import VendorTypeMap, VendorCategoryMap
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class VendorTypeMapInline(admin.TabularInline):

    model = VendorTypeMap
    extra = 1


class VendorCategoryMapInline(admin.TabularInline):

    model = VendorCategoryMap
    extra = 1


class VendorAdmin(admin.ModelAdmin):
    inlines = (VendorTypeMapInline, VendorCategoryMapInline,)
    ordering = ('id',)
    list_display = (
        'id',
        'name',
        'is_active',
        'under_review',
        'review_reason',
        'about',
        'notes_mgmt',
        'phone_info',
        'phone_support',
        'url_main',
        'url_product',
        'url_service',
        'url_support',
        'date_transitioned',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'evaluation_days',
        'evaluation_flg',
        'rank',
        'transitioned_by',
        'created_by',
        'modified_by',
        'deactivated_by',
        'deleted_by',
        'initial_account',
        'company',
        'keywords',
    )
    list_filter = (
        'is_active',
        'date_created',
        'date_modified',
        'date_deactivated',
        'date_deleted',
        'created_by',
        'modified_by',
        'deactivated_by',
        'deleted_by',
        'company',
        'keywords',
    )
    search_fields = ('name', 'parent', 'about', 'keywords')


class VendorTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class VendorCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)
