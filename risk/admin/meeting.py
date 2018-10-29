from django.contrib import admin
from risk.models.meeting import MeetingAttendee, MeetingEntry
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class MeetingAttendeeInline(admin.TabularInline):

    model = MeetingAttendee
    extra = 1


class MeetingEntryInline(admin.TabularInline):

    model = MeetingEntry
    extra = 1


class MeetingAdmin(admin.ModelAdmin):

    inlines = (MeetingAttendeeInline, MeetingEntryInline)
    list_select_related = []
    list_display = (
        'id',
        'is_active',
        'name',
        'executive_summary',
        'date_created',
        'cadence',
        'company',
        'meeting_type',
        'organizer',
    )
    list_filter = (
        'name',
        'executive_summary',
        'is_active',
        'is_deleted',
        'company',
        'meeting_type',
        'organizer',
    )
    search_fields = ('name',)


class MeetingTopicAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'topic',
        'date_created',
        'inital_meeting',
        'current_meeting',
    )
    list_filter = (
        'inital_meeting',
        'current_meeting',
    )


class MeetingTopicCommentAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'comment',
        'date_created',
        'meeting_topic',
    )
    list_filter = (
        'meeting_topic',
    )


class MeetingTopicActionAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'action',
        'date_created',
        'action_owner',
        'meeting_topic',
    )
    list_filter = (
        'meeting_topic',
    )


class MeetingTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
    )
    search_fields = ('name',)
