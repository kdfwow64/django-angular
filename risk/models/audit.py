"""Audit, Tracking & related models."""
from django.db import models


class Notification(models.Model):
    """This table describes the notifiication."""

    name = models.CharField(
        max_length=30, blank=False, help_text=('Name of the alert notifiication'),)  # Name of the notification
    description = models.TextField(
        blank=False, help_text=('Description of the alert notifiication'),)  # Name of the notification group
    # Foreign Key and Relationships
    account = models.ForeignKey('Account', on_delete=models.PROTECT, default=1, blank=False, related_name='account_notification', help_text=(
        'The account the notification was created under'),)  # By default all notificaitons  will belong to CORE and be used for all companies.  Companies may be able to add custom notifications in the future.  When added to the account, the notification will be available to all companies of the account. Only Account Admin can add alerts.  If Alerts are approved by CORE the will be available to all Accounts.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Notifications")


class NotificationGroup(models.Model):
    """This table describes the notifiication group."""

    name = models.CharField(
        max_length=30, blank=False, help_text=('Name of the notifiication group'),)  # Name of the notification
    description = models.TextField(
        blank=False, help_text=('Description of the notifiication group'),)  # Name of the notification group
    # Foreign Key and Relationships
    account = models.ForeignKey('Account', on_delete=models.PROTECT, default=1, blank=False, related_name='account_notificationgroup', help_text=(
        'The account the notificaiton group was created under'),)  # By default all alerts  will belong to CORE and be used for all companies.  Companies may be able to add custom alerts in the future.  When added to the account, the alert will be available to all companies of the account. Only Account Admin can add alerts.  If Alerts are approved by CORE the will be available to all Accounts.
    members = models.ManyToManyField('User', through='NotificationEmailDistro',
                                     through_fields=('id_notificationgroup', 'id_user'), related_name='NotificationGroupMembers', help_text=('Users that belong to the notification group'),)  # There will be specific NotificationGroups setup for CORE that will be used for all clients.  This is for application notifications, marketing notifications will be handled separately.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Notification Groups")


class NotificationEmailDistro(models.Model):
    """
    Notification Email Distro.

    Users that will be alerted if triggered by the email process
    Foreign Key and Relationships
    """

    id_notificationgroup = models.ForeignKey('NotificationGroup', on_delete=models.PROTECT, blank=False, related_name='notificaitonemaildistro', help_text=(
        'Alert used for the email notification'),)
    id_user = models.ForeignKey('User', on_delete=models.PROTECT, blank=False, related_name='alertemaildistro', help_text=(
        'Users the alert will be sent to'),)

    def __str__(self):
        """String."""
        return self.notification

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Notification Email Disto Members")


class AuditChange(models.Model):
    """
    AuditChange.

    Used to capture the changes that users make to user tables that can be
    modified.
    """

    date_modified = models.DateTimeField(
        auto_now=True, null=True, help_text=('Timestamp that the change was made'),)  # Not in use
    table = models.CharField(
        max_length=128, blank=False, help_text=('Table name that the change was made'),)  # Not in use
    column = models.CharField(
        max_length=128, blank=False, help_text=('Column name that was changed'),)  # Not in use
    row = models.IntegerField(
        blank=False, help_text=('The table id that was changed'),)  # Not in use
    oldvalue = models.CharField(
        max_length=255, blank=False, help_text=('The value prior to the change'),)  # Not in use
    # Foreign Key and Relationships
    user = models.ForeignKey('User', on_delete=models.PROTECT, related_name='auditchange', help_text=(
        'User id for the user that made the change'),)
    account = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='auditchange', help_text=(
        'Account id for the account that was changed'),)
    company = models.ForeignKey('Company', on_delete=models.PROTECT, null=True, related_name='auditchange', help_text=(
        'Company id for the company that was changed'),)

    class Meta:
        """Meta class."""
        ordering = ['user', 'date_modified']
        indexes = [
            models.Index(fields=['date_modified'], name='date_modified_idx'), ]
        verbose_name_plural = ("Audit Changes")

    def __str__(self):
        """String."""
        return self.table


class Snapshot(models.Model):
    """
    Snapshot.

    This table is used to track various marketing detail for trending over
    time the snapshot should occur weekly
    """

    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('The timestamp the snapshot was taken'),)  # Not in use
    active_accounts = models.IntegerField(
        blank=True, null=True, help_text=('Number of active accounts '),)  # Not in use
    active_companies = models.IntegerField(
        blank=True, null=True, help_text=('Number of active companies'),)  # Not in use
    active_users = models.IntegerField(
        blank=True, null=True, help_text=('Number of active users'),)  # Not in use
    company_activity = models.IntegerField(
        blank=True, null=True, help_text=('Number of companies that had activity since last snapshot '),)  # Not in use
    recent_login = models.IntegerField(
        blank=True, null=True, help_text=('Number of logins since last snapshot'),)  # Not in use
    feedback_entries = models.IntegerField(
        blank=True, null=True, help_text=('Number of feedback entries from users'),)  # Not in use
    churn_accounts = models.IntegerField(
        blank=True, null=True, help_text=('Number of accounts that did not renew'),)  # Not in use
    disabled_users = models.IntegerField(
        blank=True, null=True, help_text=('Users marked as disabled from active companies'),)  # Not in use
    register_number = models.IntegerField(
        blank=True, null=True, help_text=('Number of active registers'),)  # Not in use
    entry_number = models.IntegerField(
        blank=True, null=True, help_text=('Number of active entries'),)  # Not in use
    control_number_total = models.IntegerField(
        blank=True, null=True, help_text=('Number of controls being used'),)  # Not in use
    control_number_core = models.IntegerField(
        blank=True, null=True, help_text=('Number of controls being used specific to core'),)  # Not in use
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.date_created
