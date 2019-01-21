"""Internal Maintenace, Notifications, Reporting & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
    DefaultFieldsContext,
)


class Calendar(models.Model):
    """Calendar."""

    date = models.DateTimeField(
        help_text=('Date time'),)  # Date used to join
    year = models.IntegerField(
        help_text=('Year of the date'),)  # Year assoicated to the date
    month_number = models.IntegerField(
        help_text=('Annual month number'),)  # Month number
    month_text = models.CharField(
        max_length=15, blank=True, help_text=('Name of the month'),)  # Name of the month
    day_of_week_number = models.IntegerField(
        help_text=('Week day number'),)  # Number for the day of the week
    day_of_week_text = models.CharField(
        max_length=15, blank=True, help_text=('Name of the day'),)  # Name of the week day
    day_number_in_year = models.IntegerField(
        help_text=('Annual day number'),)  # Number for the day of the year
    day_number = models.IntegerField(
        help_text=('Month day number'),)  # Number for the day of the month
    week_in_year = models.IntegerField(
        help_text=('Annual week number'),)  # Number of the week in the year
    quarter = models.IntegerField(
        help_text=('Annual quarter number'),)  # Number of the quarter in the year
    date_text = models.CharField(
        max_length=15, blank=True, help_text=('Name of the date'),)  # Name of the date
    absolute_date = models.IntegerField(
        help_text=('Computer date'),)  # Not in use
    fiscal_quarter = models.IntegerField(
        help_text=('Fiscal quarter number'),)  # Number of quarter in the fiscal year
    fiscal_year = models.IntegerField(
        help_text=('Fiscal year number'),)  # Number of year in fiscal year
    fiscal_month = models.IntegerField(
        help_text=('Fiscal month number'),)  # Number of month in fiscal year
    week_in_fiscal = models.IntegerField(
        help_text=('Fiscal week number'),)  # Number of week in fiscal year
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.date


class CurrencyType(models.Model):
    """Currency Type."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the currency '),)  # Name of the currency type
    abbrv = models.CharField(
        max_length=5, blank=False, help_text=('Abbreviation of the currency'),)  # Abbrievation of the currency type. ISO 4217 code. IE USD,EUR,JPY,GBP
    symbol = models.CharField(
        max_length=4, blank=False, help_text=('Symbol of the currency'),)  # Symbol of the currency type, IE $,€,¥,£
    unit = models.CharField(
        max_length=15, blank=True, null=True, help_text=('Unit of the currency'),)  # Unit of currency.  IE "Dollars"
    exchange_rate = models.FloatField(blank=True, null=True, help_text=(
        'Exchange rate based on USD'),)  # This is used to determine the exchange rate base on USD for monetary calculations.
    exchange_date = models.DateTimeField(null=True, blank=True, help_text=(
        'Date the exchange rate was added to the table'),)  # Date when the exchange rate was last imported.
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Currency Types")


class EmailTemplate(DefaultFieldsCompany):
    """Email Template."""

    subject = models.CharField(
        max_length=128, blank=False, help_text=('Subject of the email template '),)  # Not in use
    body = models.TextField(
        blank=False, help_text=('Body of the email template'),)  # Not in use
    conclusion = models.TextField(
        blank=False, help_text=('Conclusion of the email template'),)  # Not in use
    signoff = models.CharField(
        max_length=30, blank=False, help_text=('Sign off of the email template '),)  # Not in use
    signature = models.CharField(
        max_length=128, blank=False, help_text=('Signature of the email template '),)  # Not in use
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Email Templates")


class Expression(models.Model):
    """Expression."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the expression '),)  # Not in use
    symbol = models.CharField(
        max_length=6, blank=False, help_text=('Symbol of the expression'),)  # Not in use
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


class IntegerType(models.Model):
    """Integer Type."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the integer type'),)  # Not in use
    description = models.TextField(
        blank=False, help_text=('Description of the integer type'),)  # Not in use
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Integer Types")


class RAGIndicator(models.Model):
    """Red, Amber, Green Indicator"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the RAG indicator'),)  # Not in use
    description = models.TextField(
        blank=False, help_text=('Description of the RAG indicator'),)  # Not in use
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("RAG Indicators")


class Cadence(DefaultFieldsCompany):
    """Cadence."""

    def __str__(self):
        """String."""
        return self.name


class TimeUnit(DefaultFieldsCategory):
    """Time Unit"""

    annual_units = models.IntegerField(null=True, blank=True, help_text=(
        'Number of units in a year'),)  # Used to for annualization logic.
    daily_units = models.DecimalField(default=1, max_digits=15, decimal_places=8, help_text=(
        'Number of units per day'),)

    class Meta:
        """Meta class."""
        ordering = ['sort_order', ]
        verbose_name_plural = ("Time Units")

    def __str__(self):
        """String."""
        return self.name


class TaskStatus(DefaultFieldsCategory):
    """Entry Task Status."""

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Task Status")

    def __str__(self):
        """String."""
        return self.name


class JobTitle(DefaultFieldsCategory):
    """Job Titles."""

    class Meta:
        """Meta class."""
        ordering = ['name']
        verbose_name_plural = ("Job Titles")

    def __str__(self):
        """String."""
        return self.name


class Appetite(DefaultFieldsCategory):
    """
    Appetite.

    How is the company defining its appetite based on the amount of risk it assumes
    """

    measure = models.CharField(
        max_length=45, blank=False, help_text=('Measurement of the appetite'),)  # The measurement of appetite occurences within a year
    minimum = models.FloatField(default=0, blank=True, help_text=(
        'The lowest percentage value for the category.'),)  # Minimum value of the appetite
    maximum = models.FloatField(default=0, blank=True, help_text=(
        'The highest percentage value for the category.  If user selects 100< they will need to put in number of occurrences per year.'),)  # Maximum value of the appetite

    class Meta:
        """Meta class."""
        ordering = ['sort_order', ]
        verbose_name_plural = ("Risk Appetite")

    def __str__(self):
        """String."""
        return self.name
