from django.contrib import admin
from django.utils.html import format_html
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
    readonly_fields = ('date_created', 'created_by', 'date_modified', 'modified_by',
                       'date_deleted', 'deleted_by', 'date_deactivated', 'deactivated_by',
                       )
    fieldsets = (
        ('Vendor Info', {
         'fields': ('name', 'abbrv', 'about', 'description', 'url_main', 'phone_info', 'email_info', 'parent')}),
        ('Vendor Misc', {
         'fields': (('url_product', 'url_service', 'url_support',), 'name_aka', 'keywords', 'stock_symbol', 'initial_account')}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('company', 'email_product', ('under_review', 'review_reason',), 'rank', ('is_active', 'is_deleted',), ('evaluation_days', 'evaluation_flg',), ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_deactivated', 'deactivated_by',), ('date_transitioned', 'transitioned_by',))}),
    )
    list_select_related = []
    list_display = (
        'id',
        'name',
        'show_vendor_url',
        'about',
        'phone_info',
        'email_info',
        'name_aka',
        'keywords',
        'parent',
        'under_review',
    )
    list_filter = (
        'is_active',
        'under_review',
    )
    search_fields = ('id', 'name', 'about', 'keywords',
                     'parent__name', 'abbrv', 'name_aka')
    ordering = ('name',)

    def show_vendor_url(self, obj):
        return format_html("<a target=\"_blank\" href='{url}'>{url}</a>", url=obj.url_main)


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
