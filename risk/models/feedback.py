"""Feedback, CSM & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
    DefaultFieldsContext,
)


class Feedback(DefaultFields):
    """Feedback.  This table manages the feedback event.  When feedback is provided an event is created and managed via this table"""

    summary = models.TextField(
        blank=True, help_text=('Summary of the feedback content'),)  # Summary will be taken from the form.
    notes = models.TextField(
        blank=True, help_text=('Notes regarding the feedback event'),)  # Note about the feedback event from management.  Not user viewable
    future_enhancement = models.BooleanField(default=False, help_text=(
        'Will the feedback be considered for future enhancment'),)  # If True, the feedback should be considered for future development or system modifications.  Not user viewable
    contact_me = models.BooleanField(default=True, help_text=(
        'Is it okay to contact the user directly'),)  # In the event more decussion needs to occur.
    phone = models.CharField(
        max_length=15, blank=False, help_text=('Phone number to contact user '),)  # Phone to use if contact_me is True
    email = models.EmailField(
        max_length=128, blank=False, unique=True, help_text=('Email address to contact user'),)  # Email to use if contact me is True.  Will not be needed if active user on the application.
    date_closed = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the feedback was completed'),)  # Not in use
    is_public = models.BooleanField(default=False, help_text=(
        'Designates whether the feedback should be made public for application users'),)
# Foreign Key and Relationships
    feedback_status = models.ForeignKey('FeedbackStatus', on_delete=models.PROTECT, null=True, related_name='feedback', help_text=(
        'Current state of the feedback effort'),)
    feedback_type = models.ForeignKey('FeedbackType', on_delete=models.PROTECT, null=True, related_name='feedback', help_text=(
        'Type of feedback provided'),)
    closed_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='completed_feedback', help_text=(
        'User that completed the feedback'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Feedback")

    def __str__(self):
        """String."""
        return self.summary


class FeedbackAnswer(DefaultFields):
    """Feedback Answers. Each type of feedback will have differnet questions for more context.  Thes answers will be tied to the question."""

    answer = models.CharField(
        max_length=255, blank=False, help_text=('Answer to the feedback question'),)  # This is the answer submitted to the feedback question
# Foreign Key and Relationships
    feedback_event = models.ForeignKey('Feedback', on_delete=models.PROTECT, null=True, related_name='feedback_eventanswer', help_text=(
        'The feedback event the answer belongs'),)
    question = models.ForeignKey('FeedbackQuestion', on_delete=models.PROTECT, null=True, related_name='feedback_questionanswer', help_text=(
        'The question that was asked for the feeedback'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Feedback Answers")

    def __str__(self):
        """String."""
        return self.answer


class FeedbackCorrespondence(DefaultFields):
    """Feedback Correspondence. Each feedback event may have a specific correspondence trail.  This table tracks that communication."""

    correspondence = models.TextField(
        blank=True, help_text=('Comment on feedback event'),)  # This will be tied to the feedback event.
# Foreign Key and Relationships
    feedback_event = models.ForeignKey('Feedback', on_delete=models.PROTECT, null=True, related_name='feedback_eventcorrespondence', help_text=(
        'The feedback event the correspondence belongs'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Feedback Correspondence")

    def __str__(self):
        """String."""
        return self.correspondence


class FeedbackQuestion(DefaultFields):
    """Feedback Questions. Each type of feedback will have differnet questions for more context"""

    question = models.CharField(
        max_length=255, blank=False, help_text=('Question used for the feedback form'),)  # This is the question used for a certain feedbakc type.
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that the questions should be displayed'),)  # Questions should be in a specific order for the form.  This will also be a factor when displaying the answer.
# Foreign Key and Relationships
    feedback_type = models.ForeignKey('FeedbackType', on_delete=models.PROTECT, null=True, related_name='feedback_type', help_text=(
        'Type of feedback the question belongs'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Feedback Questions")

    def __str__(self):
        """String."""
        return self.question


class FeedbackStatus(DefaultFieldsCompany):
    """FeedbackStatus."""

    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Feedback Status")

    def __str__(self):
        """String."""
        return self.name


class FeedbackType(DefaultFieldsCompany):
    """FeedbackType."""

    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed'),)  # Not in use
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Feedback Types")
