from django.contrib import admin
from risk.models.vendor import VendorTypeMap, VendorCategoryMap, Vendor
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
        'about',
        'phone_info',
        'phone_support',
        'url_main',
        'url_product',
        'url_service',
        'url_support',
        'initial_account',
        'keywords',
        'parent',
    )
    list_filter = (
        'is_active',
    )
    search_fields = ('name', 'about', 'keywords', 'parent__name')
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
