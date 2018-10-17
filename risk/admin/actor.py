from django.contrib import admin
from risk.models.actor import ThreatActorIntent, ThreatActorMotive
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ThreatActorIntentInline(admin.TabularInline):

    model = ThreatActorIntent
    extra = 1


class ThreatActorMotiveInline(admin.TabularInline):

    model = ThreatActorMotive
    extra = 1


class ActorAdmin(admin.ModelAdmin):

    inlines = (ThreatActorIntentInline, ThreatActorMotiveInline)
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
        'is_active',
        'is_human',
        'is_internal',
        'account',
        'desc_alt',
        'desc_form',
    )
    search_fields = ('name',)


class ActorIntentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'sort_order',
        'keywords',
        'desc_alt',
        'desc_form',
        'account',
    )
    search_fields = ('name',)


class ActorMotiveAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'account',
        'sort_order',
        'keywords',
        'desc_alt',
        'desc_form',
    )
    search_fields = ('name',)
