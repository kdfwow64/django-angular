"""Meeting & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
    DefaultFieldsContext,
)


class Meeting(DefaultFields):
    """Meeting."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the meeting'),)  # Name of the meeting.  This will be copied if meeting is cloned
    executive_summary = models.TextField(
        blank=False, help_text=('Description of the meeting'),)  # Notes regarding the meeting.  This is meeting specific
    date_start = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the meeting will start'),)  # Time the meeting will start
    date_close = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the meeting was closed'),)  # Time the meeting was closed. This will depend on when the contributor closes the meeting
    was_cancelled = models.BooleanField(default=False, help_text=(
        'Selection if the meeting was cancelled'),)  # Defines if the meeting was cancelled
    reason_cancelled = models.TextField(
        blank=True, help_text=('Reason the meeting was cancelled'),)  # Reason the meeting was cancelled
    # Foreign Key and Relationships
    cadence = models.ForeignKey('Cadence', on_delete=models.PROTECT, null=True, related_name='meeting_cadence', help_text=(
        'Cadence of the meeting '),)  # Used to determine the cadence of the meeting if it is recurring.
    company = models.ForeignKey('Company', on_delete=models.PROTECT, null=True, related_name='meeting_company', help_text=(
        'Company associated with the meeting '),)  # Company that the meeting belongs
    meeting_type = models.ForeignKey('MeetingType', on_delete=models.PROTECT, null=True, related_name='meeting_meetingtype', help_text=(
        'Type of meeting'),)  # The type of meeting
    organizer = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='meeting_organizer', help_text=(
        'Organzier of the meeting'),)  # User that created the meeting.
    attendees = models.ManyToManyField('CompanyContact', through='MeetingAttendee',
                                       through_fields=('id_meeting', 'id_companycontact'), related_name='MeetingAttedees', help_text=('Company contacts that were invited to the meeting.'),)  # Used to determine what company contacts were invited to the meeting.
    entries = models.ManyToManyField('Entry', through='MeetingEntry',
                                     through_fields=('id_meeting', 'id_entry'), related_name='MeetingEntryMap', help_text=('Entries that are discussed in the meeting.'),)  # used to define what meeting entries are associated to the meeting. You will also be able to spawn a meeting from the entry.

    def __str__(self):
        """String."""
        return self.name


class MeetingAttendee(DefaultFields):
    """Meeting POC."""

    present = models.BooleanField(default=False, help_text=(
        'Did the user attend the meeting'),)  # Not in use
    # Foreign Key and Relationships
    id_meeting = models.ForeignKey('Meeting', on_delete=models.PROTECT, null=True, related_name='meetingpoc', help_text=(
        'The meeting the POC was invited'),)
    id_companycontact = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='pocmeeting', help_text=(
        'Individual that was invited to the meeting'),)

    def __str__(self):
        """String."""
        return self.id_companycontact

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Meeting Attendee Map")


class MeetingEntry(DefaultFields):
    """Through table for Meeting.  Meeting Entries."""

    id_meeting = models.ForeignKey('Meeting', on_delete=models.PROTECT, null=True, related_name='meetingentry', help_text=(
        'The meeting the entry was discussed'),)
    id_entry = models.ForeignKey('Entry', on_delete=models.PROTECT, null=True, related_name='entrymeeting', help_text=(
        'Entry that was discussed in the meeting'),)

    def __str__(self):
        """String."""
        return self.id_entry

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Meeting Entries")


class MeetingTopic(DefaultFields):
    """Meeting Topics."""

    topic = models.TextField(
        blank=False, help_text=('Comment on the meeting topic'),)  # The topic discussed in the meeting
    date_completed = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the comment was closed'),)  # Date the topic was completed
    # Foreign Key and Relationships
    # The original meeting associated with the meeting topic.  Topics may be
    # migrated to other meetings.
    inital_meeting = models.ForeignKey('Meeting', on_delete=models.PROTECT, null=True, related_name='orginal_meeting', help_text=(
        'Meeting that the topic was originally created  under.'),)  # Topics may be moved to other meetings to be completed
    current_meeting = models.ForeignKey('Meeting', on_delete=models.PROTECT, null=True, related_name='current_meeting', help_text=(
        'Meeting that the topic is currently  under.'),)  # Topics may be moved to other meetings to be completed

    def __str__(self):
        """String."""
        return self.topic

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Meeting Topics")


class MeetingTopicComment(DefaultFields):
    """Topic Comment."""

    comment = models.TextField(
        blank=False, help_text=('Comment on the meeting topic'),)  # meeting topic comments should be sorted by created date under the meeting topic.
    date_completed = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the comment was closed'),)  # Not in use

    meeting_topic = models.ForeignKey('MeetingTopic', on_delete=models.PROTECT, null=True, related_name='meetingtopic_comment', help_text=(
        'The meeting topic the comment is associated'),)  # Meeting the topic is currently under.

    def __str__(self):
        """String."""
        return self.comment

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Topic Comments")


class MeetingTopicAction(DefaultFields):
    """Through table for MeetingTopic. Topic Action"""

    action = models.TextField(
        blank=False, help_text=('Action to be completed for the meeting'),)  # Not in use
    date_completed = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the action was closed'),)  # Not in use
    # Foreign Key and Relationships
    action_owner = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='actionowner', help_text=(
        'Individual that owns the meeting action'),)
    meeting_topic = models.ForeignKey('MeetingTopic', on_delete=models.PROTECT, null=True, related_name='meetingtopic_action', help_text=(
        'The meeting topic the action is associated'),)  # Meeting the topic is currently under

    def __str__(self):
        """String."""
        return self.action

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Topic Actions")


class MeetingType(DefaultFieldsCompany):
    """Meeting Type."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Meeting Types")
