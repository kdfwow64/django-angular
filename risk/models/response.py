"""Incident Response & related models."""
from django.db import models


class PlaybookResponsibility(models.Model):
    """User Responsibilities for the playbooks."""

    responsibility = models.TextField(
        blank=False, help_text=('Description of the responsibility for the user'),)  # The responsibility the user will have for the playbook.
    company = models.ForeignKey('Company', on_delete=models.CASCADE, default=1, null=False, blank=False, related_name='company_playbook_responsibilites', help_text=(
        'The company responsibilities that can be assigned to the playbook'),)

    def __str__(self):
        """String."""
        return self.responsibility

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Playbook Responsibilites")


class PlaybookRole(models.Model):
    """ The type of role of the company member"""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the company playbook role'),)  # Role type name for playbooks
    desc = models.TextField(
        blank=False, help_text=('Description of the company playbook role'),)  # Role type description for playbooks
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the role is active for use'),)
    role_type = models.ForeignKey(
        'PlaybookRoleType', default=1, related_name='member_roletype', on_delete=models.PROTECT, help_text=('The role type'),)  # Companies have the ability to add their own role if desired.  These will be under review for addtion to CORE.  Default submission is set to Core Company.
    company = models.ForeignKey(
        'Company', default=1, related_name='playbook_role', on_delete=models.PROTECT, help_text=('The company that the member role is managed.'),)  # Companies have the ability to add their own role if desired.  These will be under review for addtion to CORE.  Default submission is set to Core Company.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Playbook Role")


class PlaybookRoleType(models.Model):
    """ The type of role of the company member"""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the playbook member role type'),)  # Role type name for playbooks
    desc = models.TextField(
        blank=False, help_text=('Description of the company playbook member role type'),)  # Role type description for playbooks
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the member role type is active for use'),)
    company = models.ForeignKey(
        'Company', default=1, related_name='company_playbookroletype', on_delete=models.PROTECT, help_text=('The company that the member role type is managed.'),)  # Companies have the ability to add their own role types if desired.  These will be under review for addtion to CORE.  Default submission is set to Core Company.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Playbook Role Types")


class PlaybookActionType(models.Model):
    """ The type of action in the playbook"""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the company playbook action type'),)  # Action type name for playbooks
    desc = models.TextField(
        blank=False, help_text=('Description of the company playbook action type'),)  # Action type description for playbooks
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that the action type should be in for form selection'),)  # Not in use
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the action is active for use'),)
    company = models.ForeignKey(
        'Company', default=1, related_name='company_playbookactiontype', on_delete=models.PROTECT, help_text=('The company that the playbook action type is managed.'),)  # Companies may have the ability to add their own action types if desired.  These will be under review for addtion to CORE.  Default submission is set to Core Company.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Playbook Action Types")
