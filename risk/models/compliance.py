"""Compliance, Framworks & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
    DefaultFieldsContext,
)


class Compliance(DefaultFieldsCategory):
    """Compliance."""

    is_opensource = models.BooleanField(default=False, help_text=(
        'Designates whether the compliance is open for public use'),)  # If True, the TM symbol will be added to the compliance name.
    version_number = models.CharField(max_length=30, blank=True, null=True, help_text=(
        'Version indicator of the compliance type'),)  # Version number of the compliance
    year = models.IntegerField(default=0, blank=True, help_text=(
        'Year the compliance version was created'),)  # Year the version was created

    # Foreign Key and Relationships
    compliance_type = models.ForeignKey('ComplianceType', on_delete=models.PROTECT, blank=True, null=True, related_name='compliance_type', help_text=(
        'Type of compliance'),)  # This will determine the type of compliance.

    def __str__(self):
        """String."""
        return self.name


class ComplianceType(DefaultFieldsCategory):
    """ComplianceType."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Compliance Types")


class ComplianceVersion(DefaultFields):
    """ComplianceVersion."""

    version_number = models.CharField(max_length=30, blank=False, help_text=(
        'Version indicator of the compliance type'),)  # Version number of the compliance
    year = models.IntegerField(default=0, blank=True, help_text=(
        'Year the compliance version was created'),)  # Year the version was created
    # Foreign Key and Relationships
    compliance = models.ForeignKey('Compliance', on_delete=models.PROTECT, blank=False, related_name='complianceversion', help_text=(
        'Compliance.  May have multiple versions'),)  # Compliance that had this version.

    def __str__(self):
        """String."""
        return '%s %s' % (self.compliance, self.version_number)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Compliance Versions")


class ComplianceRequirement(DefaultFields):
    """Compliance."""
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order of the compliance '),)  # Not in use
    cid = models.CharField(
        max_length=128, blank=False, help_text=('Name of the compliance identifier'),)  # Not in use
    family = models.TextField(
        blank=True, null=True, help_text=('Family grouping of the compliance detail'),)  # Not in use
    description = models.TextField(
        blank=True, null=True, help_text=('Description of the compliance detail request'),)  # Not in use
    requirement = models.TextField(
        blank=True, null=True, help_text=('Requirement of the compliance detail'),)  # Not in use
    testing = models.TextField(
        blank=True, null=True, help_text=('Testing for the compliance detail requirement'),)  # Not in use
    guidance = models.TextField(
        blank=True, null=True, help_text=('Guidance for the compliance detail requirement'),)  # Not in use
    recommendation = models.TextField(
        blank=True, null=True, help_text=('Description of the compliance detail request'),)  # Not in use
    compensating_control = models.TextField(
        blank=True, null=True, help_text=('Type of compensating controls for the requirement'),)  # Not in use
    scope = models.TextField(
        blank=True, null=True, help_text=('Scoping detail for the requirement'),)  # Not in use
    priority = models.IntegerField(
        blank=True, null=True, help_text=('Priority of the compliance requirement'),)  # Not in use
    dept = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the departments '),)  # Not in use
    abbrv = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Abbreviation of the compliance detail'),)  # Not in use
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Not in use
    # Foreign Key and Relationships
    compliance = models.ForeignKey('Compliance', default=1, on_delete=models.PROTECT, blank=False, related_name='compliance', help_text=(
        'Compliance.  May have multiple versions'),)  # Compliance requirements.

    def __str__(self):
        """String."""
        return self.cid

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Compliance Requirements")


class KillChain(DefaultFieldsCategory):
    """Kill Chain."""

    def __str__(self):
        """String."""
        return self.version_number

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Kill Chain")


class Naics(models.Model):
    """Naics."""

    version = models.CharField(
        max_length=30, blank=False, help_text=('Version number of the NAICS'),)  # Not in use
    code = models.CharField(
        max_length=30, default=None, help_text=('NAICS Code'),)  # Not in use
    title = models.CharField(
        max_length=255, default=None, help_text=('Title of the NAICS'),)  # Not in use
    level = models.IntegerField(
        blank=True, null=True, help_text=('Segement of the NAICS level. Used to determine drill down into vertical'),)  # Not in use
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""

        ordering = ['version']
        indexes = [
            models.Index(fields=['version'], name='version_idx'), ]
        verbose_name_plural = ("NAICS")

    def __str__(self):
        """String."""
        return self.title

    # def get_primary_naics(self):
    #     """String."""
    #     primary = naics.objects.filter(code == self.code[:2])
    #     return self.primary.title


class PyramidofPain(DefaultFieldsCategory):
    """Pyramid of Pain."""

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Pyramid of Pain")

    def __str__(self):
        """String."""
        return self.name


''' Future use
class Framework(models.Model):
    """Form Input"""
    """Application Input"""
    name_framework = models.CharField(
        max_length=100, default=None, help_text=('Click'),)  # Not in use
    abbrv_framework = models.CharField(
        max_length=30, default=None, help_text=('Click'),)  # Not in use
    tablename_framework = models.CharField(
        max_length=30, default=None, help_text=('Click'),)  # Not in use
    desc_framework = models.TextField(
        default=None, help_text=('Click'),)  # Not in use
    verison_framework = models.CharField(
        max_length=30, default=None, help_text=('Click'),)  # Not in use
    sortorder_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l1sep_framework = models.CharField(
        max_length=5, default=None, help_text=('Click'),)  # Not in use
    l2sep_framework = models.CharField(
        max_length=5, default=None, help_text=('Click'),)  # Not in use
    l3sep_framework = models.CharField(
        max_length=5, default=None, help_text=('Click'),)  # Not in use
    l4sep_framework = models.CharField(
        max_length=5, default=None, help_text=('Click'),)  # Not in use
    l5sep_framework = models.CharField(
        max_length=5, default=None, help_text=('Click'),)  # Not in use
    l1bold_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l2bold_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l3bold_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l4bold_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l5bold_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l1italic_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l2italic_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l3italic_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l4italic_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l5italic_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l1roman_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l2roman_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l3roman_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l4roman_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    l5roman_framework = models.IntegerField(
        default=None, help_text=('Click'),)  # Not in use
    # Foreign Key and Relationships
'''
