from django.contrib import admin
from risk.models.scenario import EventTypeCIATriad
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class EventTypeCIATriadInline(admin.TabularInline):

    model = EventTypeCIATriad
    extra = 1


class EventTypeAdmin(admin.ModelAdmin):
    inlines = (EventTypeCIATriadInline,)
    list_display = (
        'id',
        'name',
        'desc',
        'sort_order',
        'keywords',
        'account',
    )
    search_fields = ('name', 'account', )


class FrequencyCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'measure',
        'rating',
        'minimum',
        'maximum',
    )
    search_fields = ('name',)


class ImpactCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'measure',
        'rating',
        'minimum',
        'maximum',
    )
    search_fields = ('name',)


class ImpactTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'sort_order',
        'keywords',
        'account',
    )
    search_fields = ('name',)


class CIATriadAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'keywords',
    )
    search_fields = ('name',)


class SeverityAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'minimum',
        'maximum',
        'sort_order',
        'keywords',
    )
    search_fields = ('name',)
