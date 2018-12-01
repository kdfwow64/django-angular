from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

# , ControlCategoryCategory
from risk.models.control import Control, ControlCategory, ControlCategoryNotification, ControlCategoryControl, ControlCategoryCIATriad
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ControlCategoryNotificationInline(admin.TabularInline):

    model = ControlCategoryNotification
    extra = 1
    fields = ('id_controlnotification',
              'is_active', 'is_deleted', 'created_by')


# class ControlCategoryControlInline(admin.TabularInline):

#     model = ControlCategoryControl
#     extra = 1
#     fields = ('id_controlcategory',
#               'is_active', 'is_deleted', 'created_by')


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
        fields = ('name', 'model_number', 'abbrv', 'description', 'vendor')

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
                       )
    # radio_fields = {'contact_type': admin.HORIZONTAL}
    autocomplete_fields = ['vendor', ]
    fieldsets = (
        ('Control Specific', {
         'fields': ('name', 'model_number', 'abbrv', 'description', 'vendor', 'control_category')}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('company', ('is_active', 'is_deleted',), ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_deleted', 'deleted_by',), ('date_deactivated', 'deactivated_by',))}),
    )
    list_select_related = []
    # inlines = (ControlCategoryControlInline,)
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


class ControlFamilyAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class ControlNotificationAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
    )
    search_fields = ('name',)


class ControlCategoryAdmin(admin.ModelAdmin):

    readonly_fields = ('date_created', 'created_by', 'date_modified', 'modified_by',
                       'date_deleted', 'deleted_by', 'date_deactivated', 'deactivated_by',
                       )
    radio_fields = {'control_category_type': admin.HORIZONTAL}
    fieldsets = (
        ('Control Category Specific', {
         'fields': ('name', 'abbrv', 'description', 'keywords', 'control_category_type', 'control_domain', 'control_family')}),
        ('Management Detail', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('company', ('is_active', 'is_deleted',), ('date_created', 'created_by',), ('date_modified', 'modified_by',), ('date_deleted', 'deleted_by',), ('date_deactivated', 'deactivated_by',))}),
    )
    inlines = (ControlCategoryNotificationInline,
               ControlCategoryCIATriadInline)
    list_select_related = []
    list_display = (
        'name',
        'description',
        'abbrv',
        'keywords',
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
    search_fields = ('name', 'keywords', 'description',)


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
