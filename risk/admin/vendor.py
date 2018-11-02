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
    list_select_related = []
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
        'rank',
        'initial_account',
        'keywords',
    )
    list_filter = (
        'is_active',
    )
    search_fields = ('name', 'about', 'keywords',)
    ordering = ('name',)


class VendorTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class VendorCategoryAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)
