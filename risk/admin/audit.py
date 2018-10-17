from django.contrib import admin
from risk.models.audit import NotificationEmailDistro
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class NotificationEmailDistroInline(admin.TabularInline):

    model = NotificationEmailDistro
    extra = 1


class NotificationAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class NotificationGroupAdmin(admin.ModelAdmin):
    inlines = (NotificationEmailDistroInline,)
    list_display = (
        'id',
        'name',
        'description',
        'account',
    )
    list_filter = ('name', 'account')


class AuditChangeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'date_modified',
        'table',
        'column',
        'row',
        'oldvalue',
        'user',
        'account',
        'company',
    )
    list_filter = ('date_modified', 'user', 'account', 'company')


class SnapshotAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'date_created',
        'active_accounts',
        'active_companies',
        'company_activity',
        'active_users',
        'recent_login',
        'feedback_entries',
        'churn_accounts',
        'disabled_users',
        'register_number',
        'entry_number',
        'control_number_total',
        'control_number_core',
    )
    list_filter = ('date_created',)
