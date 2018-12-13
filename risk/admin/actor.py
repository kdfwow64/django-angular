from django.contrib import admin
from risk.models.utility import linkify
from risk.models.actor import ThreatActorIntent, ThreatActorMotive
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ThreatActorIntentInline(admin.TabularInline):

    model = ThreatActorIntent
    extra = 1
    fields = ('id_actorintent', 'is_active', 'is_deleted', 'created_by')


class ThreatActorMotiveInline(admin.TabularInline):

    model = ThreatActorMotive
    extra = 1
    fields = ('id_actormotive', 'is_active', 'is_deleted', 'created_by')


class ActorAdmin(admin.ModelAdmin):

    inlines = (ThreatActorIntentInline, ThreatActorMotiveInline)
    list_select_related = []
    readonly_fields = ('date_created',)
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
        'is_active',
        'is_human',
        'is_internal',
        'company',
    )
    search_fields = ('name',)


class ActorIntentAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'sort_order',
        'keywords',
        'company',
    )
    search_fields = ('name',)


class ActorMotiveAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'company',
        'sort_order',
        'keywords',
    )
    search_fields = ('name',)
