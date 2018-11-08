"""Risk Scenairos & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
)


class EventType(DefaultFieldsCategory):
    """Event Type."""

    cia_triad = models.ManyToManyField("CIATriad", through='EventTypeCIATriad',
                                       through_fields=('id_eventtype', 'id_ciatriad'), related_name='EventTypeCIATriads', help_text=('Specifies what portion of the triad is associated to the event'),)  # Ties CIA Triad to the event entry.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Event Types")

    def __str__(self):
        """String."""
        return self.name


class EventTypeCIATriad(DefaultFields):
    """Event Type CIA Triad.  Define the triad to the event type"""

    id_eventtype = models.ForeignKey('EventType', on_delete=models.PROTECT, null=True, related_name='cia_eventtype', help_text=(
        'The event type the associated with the CIA Triad'),)
    id_ciatriad = models.ForeignKey('CIATriad', on_delete=models.PROTECT, null=True, related_name='eventtype_cia', help_text=(
        'The CIA Triad'),)
    context = models.TextField(
        blank=True, help_text=('Context to the event for the entry'),)  # Additional information on why the triad is associated to the eventtype.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("CIA Triad Event Types")

    def __str__(self):
        """String."""
        return self.id_eventtype


class FrequencyCategory(DefaultFieldsCategory):
    """
    Frequency.

    Chance of occurrence annually that the threat scenario would happen
    """

    measure = models.CharField(
        max_length=45, blank=False, help_text=('Measurement of the frequency'),)  # The measurement of frequency occurences within a year
    rating = models.IntegerField(
        blank=False, null=True, help_text=('Rating of the frequency for prioritizing the risk level'),)  # Used to rate the severity level of the frequency for the threat scenario.
    minimum = models.FloatField(default=0, blank=True, help_text=(
        'The lowest percentage value for the category.'),)  # Minimum value of the frequency
    maximum = models.FloatField(default=0, blank=True, help_text=(
        'The highest percentage value for the category.  If user selects 100< they will need to put in number of occurrences per year.'),)  # Maximum value of the frequency
    # Defined to help users make appropirate choices for risk relevance.
    min_year = models.CharField(max_length=128, blank=True, help_text=(
        'Number of years for the minimum value'),)
    # Defined to help users make appropirate choices for risk relevance.
    max_year = models.CharField(max_length=128, blank=True, help_text=(
        'Number of years for the minimum value'),)

    class Meta:
        """Meta class."""
        ordering = ['sort_order', ]
        verbose_name_plural = ("Frequency Categories")

    def __str__(self):
        """String."""
        return self.name


class ImpactCategory(DefaultFieldsCategory):
    """
    Impact.

    Impact table is percentage of the max financial loss a company can
    experience.  These risk_impact and risk_frequency are used to determine
    risk_rating.
    """

    measure = models.CharField(
        max_length=45, blank=False, help_text=('Measurement of the impact'),)  # Measurement of the impact
    rating = models.IntegerField(
        blank=False, null=True, help_text=('Rating of the impact for prioritizing the risk level'),)  # Rating number used to for impact
    minimum = models.FloatField(default=0, blank=True, help_text=(
        'The lowest percentage value for the category.'),)  # Minimum impact percentage
    maximum = models.FloatField(default=0, blank=True, help_text=(
        'The highest percentage value for the category.'),)  # Maximum impact percentage

    class Meta:
        """Meta class."""
        ordering = ['sort_order', ]
        verbose_name_plural = ("Impact Categories")

    def __str__(self):
        """String."""
        return self.name


class ImpactType(DefaultFieldsCategory):
    """Impact Type."""

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Impact Types")

    def __str__(self):
        """String."""
        return self.name


class CIATriad(DefaultFieldsCategory):
    """CIATriad.  Should be used when determining the threat event."""

    class Meta:
        """Meta class."""
        verbose_name_plural = ("CIA Triad")

    def __str__(self):
        """String."""
        return self.name


class SeverityCategory(DefaultFieldsCategory):
    """Severity."""

    minimum = models.FloatField(default=0, blank=True, help_text=(
        'Minimum percentage of severity'),)  # Not in use
    maximum = models.FloatField(default=0, blank=True, help_text=(
        'Maximum percentage of severity'),)  # Not in use

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Severity Categories")

    def __str__(self):
        """String."""
        return self.name
