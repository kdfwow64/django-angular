"""Risk Scenairos & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
)


class EventType(models.Model):
    """Event Type."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the event type'),)  # Name of the event
    description = models.TextField(
        blank=False, help_text=('Description of the event type'),)  # Not in use
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed'),)  # Not in use
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Not in use
    example_title1 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 1'),)  # Not in use
    example_title2 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 2'),)  # Not in use
    example_content1 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 1'),)  # Not in use
    example_content2 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 2'),)  # Not in use
    example_image1 = models.ImageField(
        help_text=('Image used to support context for example 1'), null=True, blank=True,)  # Not in use
    example_image2 = models.ImageField(
        help_text=('Image used to support context for example 2'), null=True, blank=True,)  # Not in use
    desc_alt = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Not in use
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Not in use
    # Foreign Key and Relationships
    # Companies have the ability to add their own threat event names.  These
    # will be under review for addtion to CORE.
    account = models.ForeignKey('Account', on_delete=models.PROTECT, default=1,
                                related_name='account_eventtype', help_text=('The account that the event type is related'),)
    cia_triad = models.ManyToManyField("CIATriad", through='EventTypeCIATriad',
                                       through_fields=('id_eventtype', 'id_ciatriad'), related_name='EventTypeCIATriads', help_text=('Specifies what portion of the triad is associated to the event'),)  # Ties CIA Triad to the event entry.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Event Types")


class EventTypeCIATriad(models.Model):
    """Event Type CIA Triad.  Define the triad to the event type"""

    id_eventtype = models.ForeignKey('EventType', on_delete=models.PROTECT, null=True, related_name='cia_eventtype', help_text=(
        'The event type the associated with the CIA Triad'),)
    id_ciatriad = models.ForeignKey('CIATriad', on_delete=models.PROTECT, null=True, related_name='eventtype_cia', help_text=(
        'The CIA Triad'),)
    context = models.TextField(
        blank=True, help_text=('Context to the event for the entry'),)  # Additional information on why the triad is associated to the eventtype.

    def __str__(self):
        """String."""
        return self.id_eventtype

    class Meta:
        """Meta class."""
        verbose_name_plural = ("CIA Triad Event Types")


class FrequencyCategory(models.Model):
    """
    Frequency.

    Chance of occurrence annually that the threat scenario would happen
    """

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the frequency'),)  # Name of the frequency cadence
    description = models.TextField(
        blank=False, help_text=('Description of the frequency'),)  # Description of the frequency
    measure = models.CharField(
        max_length=45, blank=False, help_text=('Measurement of the frequency'),)  # The measurement of frequency occurences within a year
    rating = models.IntegerField(
        blank=False, null=True, help_text=('Rating of the frequency for prioritizing the risk level'),)  # Used to rate the severity level of the frequency for the threat scenario.
    minimum = models.FloatField(default=0, blank=True, help_text=(
        'The lowest percentage value for the category.'),)  # Minimum value of the frequency
    maximum = models.FloatField(default=0, blank=True, help_text=(
        'The highest percentage value for the category.  If user selects 100< they will need to put in number of occurrences per year.'),)  # Maximum value of the frequency
    example_title1 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 1'),)  # Not in use
    example_title2 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 2'),)  # Not in use
    example_content1 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 1'),)  # Not in use
    example_content2 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 2'),)  # Not in use
    example_image1 = models.ImageField(
        help_text=('Image used to support context for example 1'), null=True, blank=True,)  # Not in use
    example_image2 = models.ImageField(
        help_text=('Image used to support context for example 2'), null=True, blank=True,)  # Not in use
    desc_alt = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Not in use
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Not in use
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Frequency Categories")

    def __str__(self):
        """String."""
        return self.name


class ImpactCategory(models.Model):
    """
    Impact.

    Impact table is percentage of the max financial loss a company can
    experience.  These risk_impact and risk_frequency are used to determine
    risk_rating.
    """

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the impact'),)  # Name of the impact level
    description = models.TextField(
        blank=False, help_text=('Description of the impact'),)  # Description of the impact level
    measure = models.CharField(
        max_length=45, blank=False, help_text=('Measurement of the impact'),)  # Measurement of the impact
    rating = models.IntegerField(
        blank=False, null=True, help_text=('Rating of the impact for prioritizing the risk level'),)  # Rating number used to for impact
    minimum = models.FloatField(default=0, blank=True, help_text=(
        'The lowest percentage value for the category.'),)  # Minimum impact percentage
    maximum = models.FloatField(default=0, blank=True, help_text=(
        'The highest percentage value for the category.'),)  # Maximum impact percentage
    example_title1 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 1'),)  # Not in use
    example_title2 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 2'),)  # Not in use
    example_content1 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 1'),)  # Not in use
    example_content2 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 2'),)  # Not in use
    example_image1 = models.ImageField(
        help_text=('Image used to support context for example 1'), null=True, blank=True,)  # Not in use
    example_image2 = models.ImageField(
        help_text=('Image used to support context for example 2'), null=True, blank=True,)  # Not in use
    desc_alt = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Not in use
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Not in use
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Impact Categories")


class ImpactType(models.Model):
    """Impact Type."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the impact type'),)  # Name of the impact type
    description = models.TextField(
        blank=False, help_text=('Description of the impact type'),)  # Description of the impact type
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed'),)  # Used for sorting the impact type
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Not in use
    example_title1 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 1'),)  # Not in use
    example_title2 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 2'),)  # Not in use
    example_content1 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 1'),)  # Not in use
    example_content2 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 2'),)  # Not in use
    example_image1 = models.ImageField(
        help_text=('Image used to support context for example 1'), null=True, blank=True,)  # Not in use
    example_image2 = models.ImageField(
        help_text=('Image used to support context for example 2'), null=True, blank=True,)  # Not in use
    desc_alt = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Not in use
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Not in use
    # Foreign Key and Relationships
    account = models.ForeignKey(
        'Account', on_delete=models.PROTECT, default=1, related_name='account_impacttype', help_text=('The account that the impact type is related'),)  # Companies have the ability to add their own impact type names.  These will be under review for addtion to CORE.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Impact Types")


class CIATriad(models.Model):
    """CIATriad.  Should be used when determining the threat event."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the objective'),)  # Not in use
    description = models.TextField(
        blank=False, help_text=('Description of the objective'),)  # Not in use
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Not in use
    example_title1 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 1'),)  # Not in use
    example_title2 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 2'),)  # Not in use
    example_content1 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 1'),)  # Not in use
    example_content2 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 2'),)  # Not in use
    example_image1 = models.ImageField(
        help_text=('Image used to support context for example 1'), null=True, blank=True,)  # Not in use
    example_image2 = models.ImageField(
        help_text=('Image used to support context for example 2'), null=True, blank=True,)  # Not in use
    desc_alt = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Not in use
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Not in use
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("CIA Triad")

    def __str__(self):
        """String."""
        return self.name


class SeverityCategory(models.Model):
    """Severity."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the severity'),)  # Not in use
    description = models.TextField(
        blank=False, help_text=('Description of the serverity'),)  # Not in use
    minimum = models.FloatField(default=0, blank=True, help_text=(
        'Minimum percentage of severity'),)  # Not in use
    maximum = models.FloatField(default=0, blank=True, help_text=(
        'Maximum percentage of severity'),)  # Not in use
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed'),)  # Not in use
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Not in use
    example_title1 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 1'),)  # Not in use
    example_title2 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 2'),)  # Not in use
    example_content1 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 1'),)  # Not in use
    example_content2 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 2'),)  # Not in use
    example_image1 = models.ImageField(
        help_text=('Image used to support context for example 1'), null=True, blank=True,)  # Not in use
    example_image2 = models.ImageField(
        help_text=('Image used to support context for example 2'), null=True, blank=True,)  # Not in use
    desc_alt = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Not in use
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Not in use

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Severity Categories")

    def __str__(self):
        """String."""
        return self.name
