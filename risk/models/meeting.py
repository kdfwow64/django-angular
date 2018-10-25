"""Meeting & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsCategory,
    DefaultFieldsEvaluation
)


class Meeting(models.Model):
    """Meeting."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the meeting'),)  # Name of the meeting.  This will be copied if meeting is cloned
    executive_summary = models.TextField(
        blank=False, help_text=('Description of the meeting'),)  # Notes regarding the meeting.  This is meeting specific
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether the meeting should be treated as active'),)  # Is the meeting currently active
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the meeting was created'),)  # Date the meeting was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text=('Timestamp the meeting was last modified'),)  # Date the meeting was last modified
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
    attendees = models.ManyToManyField('CompanyContact', through='MeetingAttendeeMap',
                                       through_fields=('id_meeting', 'id_companycontact'), related_name='MeetingAttedees', help_text=('Company contacts that were invited to the meeting.'),)  # Used to determine what company contacts were invited to the meeting.
    topics = models.ManyToManyField('MeetingTopic', through='MeetingTopicMap',
                                    through_fields=('id_meeting', 'id_meetingtopic'), related_name='MeetingTopicMaps', help_text=('Topics that are discussed in the meeting.'),)  # used to define what meeting topics are associated to the meeting.  Can also be used to produce an agenda.
    entries = models.ManyToManyField('Entry', through='MeetingEntryMap',
                                     through_fields=('id_meeting', 'id_entry'), related_name='MeetingEntryMap', help_text=('Entries that are discussed in the meeting.'),)  # used to define what meeting entries are associated to the meeting. You will also be able to spawn a meeting from the entry.

    def __str__(self):
        """String."""
        return self.name


class MeetingAttendeeMap(models.Model):
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


class MeetingEntryMap(models.Model):
    """Meeting Entries."""

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


class MeetingTopic(models.Model):
    """Meeting Topics."""

    topic = models.TextField(
        blank=False, help_text=('Comment on the meeting topic'),)  # The topic discussed in the meeting
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the comment was created'),)  # Date the topic was created
    date_modified = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the comment was modified'),)  # Date the topic was last modified
    date_completed = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the comment was closed'),)  # Date the topic was completed
    # Foreign Key and Relationships
    # The original meeting associated with the meeting topic.  Topics may be
    # migrated to other meetings.
    inital_meeting = models.ForeignKey('Meeting', on_delete=models.PROTECT, null=True, related_name='meetingtopic', help_text=(
        'Meeting that the topic was originally created  under.'),)
    comments = models.ManyToManyField("TopicComment", through='TopicCommentMap',
                                      through_fields=('id_meetingtopic', 'id_topiccomment'), related_name='MeetingTopicComments', help_text=('Comments associated to the topics in the meeting.'),)  # used to define what meeting topics are associated to the meeting.  Can also be used to produce an agenda.
    actions = models.ManyToManyField("TopicAction", through='TopicActionMap',
                                     through_fields=('id_meetingtopic', 'id_topicaction'), related_name='MeetingTopicActions', help_text=('The actions or takeaways from the meeting'),)  # Used to determine what actions should be completed for the meeting topic

    def __str__(self):
        """String."""
        return self.topic

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Meeting Topics")


class MeetingTopicMap(models.Model):
    """Meeting Topics."""

    id_meeting = models.ForeignKey('Meeting', on_delete=models.PROTECT, null=True, related_name='meeting_topic', help_text=(
        'The meeting the topic is associated'),)
    id_meetingtopic = models.ForeignKey('MeetingTopic', on_delete=models.PROTECT, null=True, related_name='topic_meeting', help_text=(
        'Topic tied to the meeting'),)

    def __str__(self):
        """String."""
        return self.id_meetingtopic

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Meeting Topic Map")


class TopicComment(models.Model):
    """Topic Comment."""

    comment = models.TextField(
        blank=False, help_text=('Comment on the meeting topic'),)  # Not in use
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the comment was created'),)  # Not in use
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text=('Timestamp the comment was modified'),)  # Not in use
    date_completed = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the comment was closed'),)  # Not in use

    def __str__(self):
        """String."""
        return self.comment

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Topic Comments")


class TopicAction(models.Model):
    """Topic Action"""

    action = models.TextField(
        blank=False, help_text=('Action to be completed for the meeting'),)  # Not in use
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the action was created'),)  # Not in use
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text=('Timestamp the action was modified'),)  # Not in use
    date_completed = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the action was closed'),)  # Not in use
    # Foreign Key and Relationships
    action_owner = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='actionowner', help_text=(
        'Individual that owns the meeting action'),)

    def __str__(self):
        """String."""
        return self.action

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Topic Actions")


class TopicCommentMap(models.Model):
    """Topic Comments for the meeting."""

    id_meetingtopic = models.ForeignKey('MeetingTopic', on_delete=models.PROTECT, null=True, related_name='comment_meetingtopic', help_text=(
        'The meeting the topic comment is associated'),)
    id_topiccomment = models.ForeignKey('TopicComment', on_delete=models.PROTECT, null=True, related_name='meetingtopic_comment', help_text=(
        'Topic comment tied to the meeting'),)

    def __str__(self):
        """String."""
        return self.id_topiccomment

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Topic Comment Map")


class TopicActionMap(models.Model):
    """Topic Comments for the meeting."""

    id_meetingtopic = models.ForeignKey('MeetingTopic', on_delete=models.PROTECT, null=True, related_name='action_meetingtopic', help_text=(
        'The meeting the topic action is associated'),)
    id_topicaction = models.ForeignKey('TopicAction', on_delete=models.PROTECT, null=True, related_name='meetingtopic_comment', help_text=(
        'Topic action tied to the meeting'),)

    def __str__(self):
        """String."""
        return self.id_topicaction

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Topic Action Map")


class MeetingType(models.Model):
    """Meeting Type."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the meeting type'),)  # Name of the meeting type
    description = models.TextField(
        blank=False, help_text=('Description of the meeting type'),)  # Description of the meeting type
    desc_alt = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Text hovering discription
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Description used for the form.
    company = models.ForeignKey('Company', on_delete=models.PROTECT, default=1, blank=False, related_name='companymeetingtype', help_text=(
        'Company id for the meeting type'),)  # Meeting types that belong to Core will be available for all companies to use.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Meeting Types")
