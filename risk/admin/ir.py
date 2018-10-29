from django.contrib import admin
# from risk.models.response import
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class PlaybookRoleAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description',
                    'is_active', 'role_type', 'company',)
    search_fields = ('name',)


class PlaybookRoleTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description', 'is_active', 'company',)
    search_fields = ('name',)


class PlaybookActionTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description', 'sort_order',
                    'is_active', 'company',)
    search_fields = ('name',)


class PlaybookResponsibilityAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'responsibility',
        'company',
    )
    list_filter = (
        'company',
    )
