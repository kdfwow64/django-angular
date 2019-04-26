from django.contrib import admin
from risk.models.utility import linkify
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class CalendarAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'date',
        'year',
        'month_number',
        'month_text',
        'day_of_week_number',
        'day_of_week_text',
        'day_number_in_year',
        'day_number',
        'week_in_year',
        'quarter',
        'date_text',
        'absolute_date',
        'fiscal_quarter',
        'fiscal_year',
        'fiscal_month',
        'week_in_fiscal',
    )
    list_filter = ('date',)


class CurrencyTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'abbrv', 'symbol', 'unit', 'exchange_rate')
    search_fields = ('name',)


class EmailTemplateAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'subject',
        'body',
        'conclusion',
        'signoff',
        'signature',
    )
    search_fields = ('name',)


class ExpressionAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'symbol',
    )
    search_fields = ('name',)


class IntegerTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class RAGIndicatorAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description', 'color', 'color_hex')
    search_fields = ('name',)


class CadenceAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
    )
    search_fields = ('name',)


class TimeUnitAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'annual_units',
        'daily_units',
        'sort_order',
    )
    search_fields = ('name',)
    ordering = ['sort_order', ]


class TaskStatusAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description', 'sort_order')
    search_fields = ('name',)


class JobTitleAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description',
                    'is_active', 'is_deleted', 'is_test', 'keywords')
    search_fields = ['name', 'keywords', ]
    ordering = ['name']


class AppetiteAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'measure',
        'sort_order',
        'minimum',
        'maximum',
    )
    search_fields = ('name',)
