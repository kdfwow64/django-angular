from django.contrib import admin
from risk.models.utility import linkify
from risk.models.scenario import EventTypeCIATriad
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class EventTypeCIATriadInline(admin.TabularInline):

    model = EventTypeCIATriad
    extra = 1


class EventTypeAdmin(admin.ModelAdmin):
    inlines = (EventTypeCIATriadInline,)
    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
        'keywords',
        'company',
    )
    search_fields = ('name', 'account', )


class FrequencyCategoryAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'measure',
        'rating',
        'sort_order',
        'minimum',
        'maximum',
        'min_year',
        'max_year',
    )
    search_fields = ('name',)


class ImpactCategoryAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'measure',
        'rating',
        'sort_order',
        'minimum',
        'maximum',
    )
    search_fields = ('name',)


class ImpactTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
        'keywords',
        'company',
    )
    search_fields = ('name',)


class MitigationImpactTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
        'keywords',
        'company',
    )
    search_fields = ('name',)


class MitigationFrequencyTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
        'keywords',
        'company',
    )
    search_fields = ('name',)


class CIATriadAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
    )
    search_fields = ('name',)


class SeverityCategoryAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'measure',
        'minimum',
        'maximum',
        'sort_order',
        'keywords',
    )
    search_fields = ('name',)
