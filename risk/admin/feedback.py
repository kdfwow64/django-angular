from django.contrib import admin
from risk.models.utility import linkify
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class FeedbackAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'notes',
        'future_enhancement',
        'contact_me',
        'phone',
        'email',
        'feedback_status',
        'feedback_type',
        'is_active',
        'is_deleted',
        'is_public',
    )
    list_filter = (
        'future_enhancement',
        'feedback_status',
        'feedback_type',
    )


class FeedbackAnswerAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'answer',
        'created_by',
        'feedback_event',
        'question',
    )
    list_list = (
        'feedback_event',
    )


class FeedbackCorrespondenceAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'correspondence',
        'feedback_event',
    )
    list_filter = (
        'correspondence',
        'feedback_event',
    )


class FeedbackQuestionAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'question',
        'is_active',
        'is_deleted',
        'feedback_type',
    )
    list_filter = (
        'is_active',
        'feedback_type',
    )


class FeedbackStatusAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


class FeedbackTypeAdmin(admin.ModelAdmin):

    list_select_related = []
    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
    )
    search_fields = ('name',)
