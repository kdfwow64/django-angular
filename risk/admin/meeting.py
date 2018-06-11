from django.contrib import admin
from risk.models.meeting import MeetingAttendeeMap, MeetingEntryMap, MeetingTopicMap, TopicActionMap, TopicCommentMap
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class MeetingAttendeeMapInline(admin.TabularInline):

    model = MeetingAttendeeMap
    extra = 1


class MeetingEntryMapInline(admin.TabularInline):

    model = MeetingEntryMap
    extra = 1


class MeetingTopicMapInline(admin.TabularInline):

    model = MeetingTopicMap
    extra = 1


class TopicCommentMapInline(admin.TabularInline):

    model = TopicCommentMap
    extra = 1


class TopicActionMapInline(admin.TabularInline):

    model = TopicActionMap
    extra = 1


class MeetingAdmin(admin.ModelAdmin):

    inlines = (MeetingAttendeeMapInline,
               MeetingTopicMapInline, MeetingEntryMapInline)
    list_display = (
        'id',
        'is_active',
        'name',
        'executive_summary',
        'date_created',
        'date_modified',
        'date_start',
        'date_close',
        'was_cancelled',
        'reason_cancelled',
        'cadence',
        'company',
        'meeting_type',
        'organizer',
    )
    list_filter = (
        'is_active',
        'date_created',
        'date_modified',
        'date_start',
        'date_close',
        'was_cancelled',
        'cadence',
        'company',
        'meeting_type',
        'organizer',
    )
    search_fields = ('name',)


class MeetingTopicAdmin(admin.ModelAdmin):

    inlines = (TopicCommentMapInline, TopicActionMapInline,)
    list_display = (
        'id',
        'topic',
        'date_created',
        'date_modified',
        'date_completed',
        'inital_meeting',

    )
    list_filter = (
        'date_created',
        'date_modified',
        'date_completed',
        'inital_meeting',
    )


class TopicCommentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'comment',
        'date_created',
        'date_modified',
        'date_completed',
    )
    list_filter = (
        'date_created',
        'date_modified',
        'date_completed',
    )


class TopicActionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'action',
        'date_created',
        'date_modified',
        'date_completed',
        'action_owner',
    )
    list_filter = (
        'date_created',
        'date_modified',
        'date_completed',
        'action_owner',
    )


class MeetingTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
    )
    search_fields = ('name',)
