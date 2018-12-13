from django.contrib import admin
from django.utils.html import format_html
from risk.models.utility import linkify
from risk.models.vendor import VendorTypeMap, VendorCategoryMap, Vendor
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class VendorTypeMapInline(admin.TabularInline):

    model = VendorTypeMap
    extra = 1
    fields = ('id_vendortype',
              'is_active', 'is_deleted', 'created_by')


class VendorCategoryMapInline(admin.TabularInline):

    model = VendorCategoryMap
    extra = 1
    fields = ('id_vendorcategory',
              'is_active', 'is_deleted', 'created_by')


class VendorAdmin(admin.ModelAdmin):
    inlines = (VendorTypeMapInline, VendorCategoryMapInline,)
    readonly_fields = ('date_created', 'created_by', 'date_modified', 'modified_by',
                       'date_deleted', 'deleted_by', 'date_deactivated', 'deactivated_by',
                       'id',)
    fieldsets = (
        ('Vendor Info', {
         'fields': ('name', 'abbrv', 'about', 'description', 'url_main', 'phone_info', 'email_info', 'parent')}),
        ('Vendor Misc', {
         'fields': (('url_products', 'url_contact', 'url_about_us',), 'name_aka', 'keywords', 'stock_symbol', 'initial_account')}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('id', 'company', 'email_product', ('under_review', 'review_reason',), 'rank', ('is_active', 'is_deleted',), ('evaluation_days', 'evaluation_flg',), ('url_crawler_days', 'url_crawler_flg', 'date_url_crawler',), ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_deactivated', 'deactivated_by',), ('date_transitioned', 'transitioned_by',))}),
    )
    list_select_related = []
    list_display = (
        'name',
        'show_vendor_url',
        'about',
        'phone_info',
        'email_info',
        'name_aka',
        'keywords',
        # linkify('parent'),
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
