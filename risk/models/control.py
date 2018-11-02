"""Controls & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
)


class Control(DefaultFieldsCompany):
    """Controls used to mitigate risk."""

    abbrv = models.CharField(max_length=30, null=True, blank=True, help_text=(
        'Abbreviation of the control'),)  # Abbreviation of the name field.
    model_number = models.CharField(
        max_length=128, null=True, blank=True, help_text=('Model number of the control'),)  # The model will be used to further clarify the type of control being used if it is applicable.  A combination of the control and the model number will make the record unique. IE Cisco ASA "2505".
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=True, related_name='controldetail', help_text=(
        'Vendor that produces the control '),)  # Vendor that makes or maintains the control.  If the account manages/creates the control then this should be listed as Self.
    # control_category = models.ForeignKey(
    #     'ControlCategory', on_delete=models.PROTECT, null=True,  related_name='controlcategory_control', help_text=('The category of the vendors control'),)  # Category the control is associated.  Used to correlate control information.
    control_protection = models.ManyToManyField("ControlCategory", through='ControlCategoryProtection', through_fields=('id_control', 'id_controlcategory'), related_name='ControlCategories', help_text=(
        'The protection categories that the control provides'),)  # Used to categorize the protection the control performs

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        unique_together = (('name', 'model_number'),)
        verbose_name_plural = ("Controls")


class ControlCategoryProtection(DefaultFields):
    """Control Category Protection.  Used determine what type of protection the control provides"""

    # Foreign Key and Relationships
    id_control = models.ForeignKey('Control', on_delete=models.PROTECT, null=True, related_name='controlcategory_protection', help_text=(
        'The control'),)
    id_controlcategory = models.ForeignKey('ControlCategory', on_delete=models.PROTECT, null=True, related_name='protection_controlcategory', help_text=(
        'Category of control'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Protections")


class ControlCategory(DefaultFieldsCategory):
    """Control Category."""

    control_category_type = models.ForeignKey('ControlCategoryType', on_delete=models.PROTECT, null=True, related_name='type_controlcategory', help_text=(
        'Type of control category'),)
    control_domain = models.ForeignKey('ControlDomain', default=1, on_delete=models.PROTECT, null=True, related_name='category_controldomain', help_text=(
        'Type of control category domain'),)
    available_operation = models.ManyToManyField("ControlOperation", through='ControlCategoryOperation', through_fields=('id_controlcategory', 'id_controloperation'), related_name='ControlOperationalLevel', help_text=(
        'The level at which the control category operates'),)  # Control categories can have multiple operation levels.  This field is used show what may be available for the control.
    available_function = models.ManyToManyField("ControlFunction", through='ControlCategoryFunction', through_fields=('id_controlcategory', 'id_controlfunction'), related_name='ControlFunctionalLevel', help_text=(
        'The level at which the control category functions'),)  # Control categories can have multiple functions.  This field is used show what may be available for the control.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Categories")

    def __str__(self):
        return self.name


class ControlCategoryType(DefaultFieldsCategory):
    """Control Category Type."""

    def __str__(self):
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Category Types")


class ControlFunction(DefaultFieldsCategory):
    """Control Function.  This the type of function the control performs for the company.  Some controls support multiple type of functionality which would result in different types of measurements for the controls effectiveness.  Careful consideration should be taken defining these terms so client messaging is not diluted.  Available functions for the control category will be mapped in the ControlCategory.  What functions are used for the control by the company will be mapped at the CompanyControl."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Functions")


class ControlCategoryFunction(DefaultFields):
    """Control Category Function.Used to define what functions are availabe for the user to chose"""

    # Foreign Key and Relationships
    id_controlcategory = models.ForeignKey('ControlCategory', on_delete=models.PROTECT, null=True, related_name='category_control_function', help_text=(
        'Category of control'),)
    id_controlfunction = models.ForeignKey('ControlFunction', on_delete=models.PROTECT, null=True, related_name='function_control_category', help_text=(
        'Functional uses of the control'),)
    description = models.TextField(
        blank=False, help_text=('Description of the function the control performs'),)  # This field will help the user better understand how they are using the control defined.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Available Control Functions")


class ControlOperation(DefaultFieldsCompany):
    """Control Operation.  This will determine the operating stage of the control to prevent risk.  Choices are preventive, detective, corrective, or predictive """

    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that the operational level should be in for form selection'),)  # Sort order for form selection.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Operation")


class ControlCategoryOperation(DefaultFields):
    """Control Category Operation.  Used to define what operation levels are availabe for the user to chose"""

    # Foreign Key and Relationships
    id_controlcategory = models.ForeignKey('ControlCategory', on_delete=models.PROTECT, null=True, related_name='category_control_operation', help_text=(
        'Category of control'),)
    id_controloperation = models.ForeignKey('ControlOperation', on_delete=models.PROTECT, null=True, related_name='operation_control_category', help_text=(
        'Opeational level of the control'),)
    description = models.TextField(
        blank=False, help_text=('Description of the how the control would operate at the selected level'),)  # This field will help the user better understand how they are using the control defined.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Available Control Operation Levels")


class ControlDomain(DefaultFieldsCategory):
    """Control Domain.  This is the domain the control belongs."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Domains")


class ControlCsc(DefaultFields):
    """Control CSC."""

    version = models.CharField(
        max_length=30, blank=False, help_text=('Version of the CSC control model'),)  # Version of the CSC publication
    number = models.CharField(
        max_length=30, blank=False, help_text=('Number of the CSC'),)  # The control number for the version.
    description = models.TextField(
        blank=True, help_text=('Description of the CSC Control'),)  # The description of the CSC control.
    # Foreign Key and Relationships
    control_csc_family = models.ForeignKey('ControlCscFamily', on_delete=models.PROTECT, null=True, related_name='controlcsc', help_text=(
        'Family that the CSC control belongs '),)

    def __str__(self):
        """String."""
        return self.desc

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control CSC")


class ControlCscFamily(DefaultFieldsCompany):
    """Control CSC Family."""
    notes = models.TextField(
        blank=True, null=True,  help_text=('Notes associated wtih the indicator'),)  # Not in use

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control CSC Families")


# class DependencyType(DefaultFieldsCompany):
#     """Dependency Type"""

#     DEPENDENT_CHOICES = (
#         ('contact', 'Contact'),
#         ('team', 'Team'),
#         ('vendor', 'Vendor'),
#     )
#     # Used to separate dependency types for select options for CompanyControl
#     # m2m dependents.
#     dependent = models.CharField(
#         max_length=7, choices=DEPENDENT_CHOICES, default='CONTACT')

#     def __str__(self):
#         """String."""
#         return self.name

#     class Meta:
#         """Meta class."""
#         verbose_name_plural = ("Dependency Types")


class DependencyEffort(DefaultFieldsCompany):
    """Future USE?  Dependency Effort.  This field is used to better describes the assocation the dependcy has with the control"""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Dependency Efforts")
