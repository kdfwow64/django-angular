from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.html import format_html
from risk.models.utility import linkify
# , ControlCategoryCategory
from risk.models.control import Control, ControlCategory, ControlCategoryResponse, ControlCategoryFunction, ControlCategoryFeature, ControlCategoryControl, ControlCategoryCIATriad, ControlOnusMethod, ControlDeliveryMethod, ControlBillingMethod
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ControlCategoryResponseInline(admin.TabularInline):

    model = ControlCategoryResponse
    extra = 1
    fields = ('id_controlresponse',
              'is_active', 'is_deleted', 'created_by')


class ControlCategoryFunctionInline(admin.TabularInline):

    model = ControlCategoryFunction
    extra = 1
    fields = ('id_controlfunction',
              'is_active', 'is_deleted', 'created_by')


class ControlCategoryFeatureInline(admin.TabularInline):

    model = ControlCategoryFeature
    extra = 1
    fields = ('id_controlfeature', 'is_key',
              'is_active', 'is_deleted', 'created_by')


class ControlOnusMethodInline(admin.TabularInline):

    model = ControlOnusMethod
    extra = 1
    fields = ('id_onus_method',
              'is_active', 'is_deleted', 'created_by')


class ControlDeliveryMethodInline(admin.TabularInline):

    model = ControlDeliveryMethod
    extra = 1
    fields = ('id_delivery_method',
              'is_active', 'is_deleted', 'created_by')


class ControlBillingMethodInline(admin.TabularInline):

    model = ControlBillingMethod
    extra = 1
    fields = ('id_billing_method',
              'is_active', 'is_deleted', 'created_by')


class ControlCategoryCIATriadInline(admin.TabularInline):

    model = ControlCategoryCIATriad
    extra = 1
    fields = ('id_ciatriad',
              'is_active', 'is_deleted', 'created_by')


class ControlAdminForm(forms.ModelForm):
    control_category = forms.ModelMultipleChoiceField(
        queryset=ControlCategory.objects.order_by('name').all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Control Categories',
            is_stacked=False
        )
    )

    class Meta:
        model = Control
        fields = ('name', 'url', 'abbrv', 'name_aka',
                  'description', 'vendor')

    def __init__(self, *args, **kwargs):
        super(ControlAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields[
                'control_category'].initial = self.instance.categories.all()
            self.fields['control_category'].queryset = self.fields[
                'control_category'].queryset.exclude(pk=self.instance.pk)

    def save(self, commit=True):
        control = super(ControlAdminForm, self).save(commit=False)
        if commit:
            control.save()

        if control.pk:
            control_category = self.cleaned_data['control_category']
            print(control_category)
            for category in control.categories.all():
                if category in control_category.all():  # Already in category, no need to handle
                    control_category = control_category.exclude(pk=category.pk)
                else:  # Remove if removed in front-end
                    ControlCategoryControl.objects.get(
                        id_control=control, id_controlcategory=category).delete()

            for category in control_category.all():  # Add new categories
                ControlCategoryControl.objects.create(
                    id_control=control, id_controlcategory=category)

        return control


class ControlAdmin(admin.ModelAdmin):
    form = ControlAdminForm
    readonly_fields = ('date_created', 'created_by', 'date_modified', 'modified_by',
                       'date_deleted', 'deleted_by', 'date_deactivated', 'deactivated_by',
                       'id',)
    #radio_fields = {'billing_method': admin.HORIZONTAL}
    autocomplete_fields = ['vendor', ]
    fieldsets = (
        ('Control Specific', {
         'fields': ('name', 'abbrv', 'description', 'name_aka', 'url', 'vendor', 'control_category')}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('id', 'company', ('is_active', 'is_deleted',), ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_deleted', 'deleted_by',), ('date_deactivated', 'deactivated_by',))}),
    )
    list_select_related = []
    inlines = (ControlOnusMethodInline, ControlDeliveryMethodInline,
               ControlBillingMethodInline,)
    list_display = (
        'name',
        'description',
        'show_control_url',
        'name_aka',
        linkify(field_name='vendor'),
        'keywords',
        'company',
    )
    search_fields = ('name', 'abbrv', 'description', 'name_aka', 'keywords')
    list_filter = ('name', 'vendor', 'company')

    def show_control_url(self, obj):
        return format_html("<a target=\"_blank\" href='{url}'>{url}</a>", url=obj.url)


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


class ControlFamilyAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class ControlResponseAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'example1',
    )
    search_fields = ('name',)


class ControlFunctionAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'example1',
    )
    search_fields = ('name',)


class ControlFeatureAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'example1',
    )
    search_fields = ('name',)


class ControlCategoryAdmin(admin.ModelAdmin):

    readonly_fields = ('date_created', 'created_by', 'date_modified', 'modified_by',
                       'date_deleted', 'deleted_by', 'date_deactivated', 'deactivated_by',
                       'id',)
    radio_fields = {'control_category_type': admin.HORIZONTAL}
    fieldsets = (
        ('Control Category Specific', {
         'fields': ('name', 'abbrv', 'description', 'keywords', 'core_expectation', 'control_category_type', 'control_domain', 'control_family')}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('id', 'company', ('is_active', 'is_deleted',), ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_deleted', 'deleted_by',), ('date_deactivated', 'deactivated_by',))}),
    )
    inlines = (ControlCategoryResponseInline, ControlCategoryResponseInline,
               ControlCategoryCIATriadInline, ControlCategoryFeatureInline, ControlCategoryFunctionInline
               )
    list_select_related = []
    list_display = (
        'name',
        'description',
        'abbrv',
        'core_expectation',
        'control_category_type',
        'control_domain',
        'control_family',
        'company',
    )
    list_filter = (
        'control_category_type',
        'control_domain',
        'control_family',
        'company',

    )
    search_fields = ('name', 'keywords', 'description', 'abbrv')


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


class OnusMethodAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'abbrv',
        'keywords',
    )
    search_fields = ('sort_order',)


class DeliveryMethodAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'abbrv',
        'keywords',
    )
    search_fields = ('sort_order',)


class BillingMethodAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'abbrv',
        'keywords',
    )
    search_fields = ('sort_order',)
