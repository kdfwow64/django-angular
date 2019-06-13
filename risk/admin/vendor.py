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
              'is_active', 'is_deleted', 'is_test', 'created_by')


class VendorCategoryMapInline(admin.TabularInline):

    model = VendorCategoryMap
    extra = 1
    fields = ('id_vendorcategory',
              'is_active', 'is_deleted', 'is_test', 'created_by')


class VendorAdmin(admin.ModelAdmin):
    inlines = (VendorTypeMapInline, VendorCategoryMapInline,)
    readonly_fields = ('date_created', 'created_by', 'date_modified', 'modified_by',
                       'date_deleted', 'deleted_by', 'date_activated', 'activated_by', 'date_deactivated', 'deactivated_by',
                       'id',)
    fieldsets = (
        ('Vendor Info', {
         'fields': ('name', 'abbrv', 'about', 'description', 'url_main', ('url_contact', 'url_about_us',), ('url_products', 'url_services', 'url_solutions',), 'name_aka', 'parent')}),
        ('Vendor Misc', {
         'fields': ('phone_info', 'email_info', 'keywords', 'stock_symbol', 'year_established', 'initial_account')}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('id', 'company', 'email_product', ('under_review', 'review_reason',), 'rank', ('is_active', 'is_deleted', 'is_test',), ('evaluation_days', 'evaluation_flg',), ('url_crawler_days', 'url_crawler_flg', 'date_url_crawler',), 'approved_by', ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_activated', 'activated_by',), ('date_deactivated', 'deactivated_by',), ('date_transitioned', 'transitioned_by',))}),
    )
    list_select_related = []
    list_display = (
        'id',
        'get_vendor_acronym',
        'show_vendor_url',
        'show_about_url',
        'show_contact_url',
        'show_products_url',
        'show_services_url',
        'show_solutions_url',
        'name_aka',
        linkify(field_name='parent'),
        # 'parent',
        'under_review',
        'review_reason',
    )
    list_filter = (
        'is_active',
        'under_review',
    )
    search_fields = ('id', 'name', 'about', 'keywords',
                     'parent__name', 'abbrv', 'name_aka')
    ordering = ('name',)

    def show_vendor_url(self, obj):
        if obj.url_main:
            return format_html("<a target=\"_blank\" href='{url}'>Website</a>", url=obj.url_main)
        else:
            return 'Needed'

    def show_about_url(self, obj):
        if obj.url_about_us:
            return format_html("<a target=\"_blank\" href='{url}'>About Us</a>", url=obj.url_about_us)
        else:
            return 'Needed'

    def show_contact_url(self, obj):
        if obj.url_contact:
            return format_html("<a target=\"_blank\" href='{url}'>Contact Us</a>", url=obj.url_contact)
        else:
            return 'Needed'

    def show_products_url(self, obj):
        if obj.url_products:
            return format_html("<a target=\"_blank\" href='{url}'>Products</a>", url=obj.url_products)
        else:
            return 'Needed'

    def show_services_url(self, obj):
        if obj.url_services:
            return format_html("<a target=\"_blank\" href='{url}'>Services</a>", url=obj.url_services)
        else:
            return 'Needed'

    def show_solutions_url(self, obj):
        if obj.url_solutions:
            return format_html("<a target=\"_blank\" href='{url}'>Solutions</a>", url=obj.url_solutions)
        else:
            return 'Needed'


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
