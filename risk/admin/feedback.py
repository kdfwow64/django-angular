from django.contrib import admin
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'notes',
        'future_enhancement',
        'contact_me',
        'phone',
        'email',
        'date_created',
        'date_closed',
        'submitted_by',
        'feedback_status',
        'feedback_type',
        'closed_by',
    )
    list_filter = (
        'future_enhancement',
        'contact_me',
        'date_created',
        'date_closed',
        'submitted_by',
        'feedback_status',
        'feedback_type',
        'closed_by',
    )


class FeedbackAnswerAdmin(admin.ModelAdmin):

    list_display = (
        'answer',
        'date_submitted',
        'created_by',
        'feedback_event',
        'question',
    )
    list_list = (
        'date_submitted',
        'created_by',
        'feedback_event',
    )


class FeedbackCorrespondenceAdmin(admin.ModelAdmin):

    list_display = (
        'correspondence',
        'date_submitted',
        'created_by',
        'feedback_event',
    )
    list_filter = (
        'correspondence',
        'date_submitted',
        'created_by',
        'feedback_event',
    )


class FeedbackQuestionAdmin(admin.ModelAdmin):

    list_display = (
        'question',
        'is_active',
        'sort_order',
        'date_created',
        'created_by',
        'feedback_type',
    )
    list_filter = (
        'is_active',
        'date_created',
        'created_by',
        'feedback_type',
    )


class FeedbackStatusAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'desc')
    search_fields = ('name',)


class FeedbackTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'sort_order',
    )
    search_fields = ('name',)
