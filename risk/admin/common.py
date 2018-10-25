from django.contrib import admin
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class CalendarAdmin(admin.ModelAdmin):

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

    list_display = ('id', 'name', 'abbrv', 'symbol', 'unit', 'exchange_rate')
    search_fields = ('name',)


class EmailTemplateAdmin(admin.ModelAdmin):

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

    list_display = (
        'id',
        'name',
        'symbol',
    )
    search_fields = ('name',)


class IntegerTypeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class RAGIndicatorAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class CadenceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
    )
    search_fields = ('name',)


class TimeUnitAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
    )
    search_fields = ('name',)


class TaskStatusAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description', 'sort_order')
    search_fields = ('name',)
