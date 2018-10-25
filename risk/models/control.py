"""Controls & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsCategory,
    DefaultFieldsEvaluation
)


class Control(models.Model):
    """Controls used to mitigate risk."""

    name = models.CharField(
        max_length=128, help_text=('Brand name of the control details'),)  # This should be the name of the control that is specified by the vendor.  Examples would be "Cisco ASA" 2505
    model_number = models.CharField(
        max_length=128, null=True, blank=True, help_text=('Model number of the control'),)  # The model will be used to further clarify the type of control being used if it is applicable.  A combination of the control and the model number will make the record unique. IE Cisco ASA "2505".
    description = models.TextField(
        blank=False, help_text=('Description of the vendor control detail'),)  # Description of the control. Example may be firewall
    abbrv = models.CharField(
        max_length=30, blank=True, help_text=('Abbreviation of the vendor control name'),)  # Abbrevation of the control.  Used for reporting if present.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the control is active for use'),)
    # Foreign Key and Relationships
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=True, related_name='controldetail', help_text=(
        'Vendor that produces the control '),)  # Vendor that makes or maintains the control.  If the account manages/creates the control then this should be listed as Self.
    account = models.ForeignKey(
        'Account', default=1, on_delete=models.PROTECT, related_name='account_control', help_text=('The account that the control is related'),)  # Account associated with the control.  Controls belonging to core will be seen by all accounts.
    control_category = models.ForeignKey(
        'ControlCategory', on_delete=models.PROTECT, null=True,  related_name='controlcategory_control', help_text=('The category of the vendors control'),)  # Category the control is associated.  Used to correlate control information.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        unique_together = (('name', 'model_number'),)
        verbose_name_plural = ("Controls")


class ControlCategory(models.Model):
    """Control Category."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the control category'),)  # Not in use
    description = models.TextField(
        blank=True, null=True, help_text=('Description of the asset'),)  # Not in use
    abbrv = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Abbreviation of the name'),)  # Not in use
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that the asset type should be in for form selection'),)  # Not in use
    has_resilience = models.BooleanField(
        default=False, help_text=('Designates whether the control will have a resilience option'),)  # If set to True the control has the optiion resilience setting in the companycontrol.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Not in use
    date_modified = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Not in use
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the individual was deactivated'),)  # Not in use
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Not in use
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
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='created_controlcategory', help_text=(
        'User id of the user that created the field'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_controlcategory', help_text=(
        'User id that last modified the field'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_controlcategory', help_text=(
        'User id if deactivated by another user'),)
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deleted_controlcategory', help_text=(
        'User id if deleted by another user'),)
    control_category_type = models.ForeignKey('ControlCategoryType', on_delete=models.PROTECT, null=True, related_name='type_controlcategory', help_text=(
        'Type of control category'),)
    control_domain = models.ForeignKey('ControlDomain', on_delete=models.PROTECT, null=True, related_name='category_controldomain', help_text=(
        'Type of control category domain'),)
    account = models.ForeignKey(
        'Account', on_delete=models.PROTECT, default=1, related_name='account_contorlcategory', help_text=('The account that the control category is related'),)  # Companies have the ability to add their own control category name.  These will be under review for addtion to CORE.
    available_operation = models.ManyToManyField("ControlOperation", through='ControlCategoryOperation', through_fields=('id_controlcategory', 'id_controloperation'), related_name='ControlOperationalLevel', help_text=(
        'The level at which the control category operates'),)  # Control categories can have multiple operation levels.  This field is used show what may be available for the control.
    available_function = models.ManyToManyField("ControlFunction", through='ControlCategoryFunction', through_fields=('id_controlcategory', 'id_controlfunction'), related_name='ControlFunctionalLevel', help_text=(
        'The level at which the control category functions'),)  # Control categories can have multiple functions.  This field is used show what may be available for the control.

    def __str__(self):
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Categories")


class ControlCategoryType(models.Model):
    """Control Category Type."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Type control category'),)  # Not in use
    description = models.TextField(
        blank=True, null=True, help_text=('Description of the asset'),)  # Not in use
    abbrv = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Abbreviation of the name'),)  # Not in use
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that the asset type should be in for form selection'),)  # Not in use
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

    def __str__(self):
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Category Types")


class ControlFunction(models.Model):
    """Control Function.  This the type of function the control performs for the company.  Some controls support multiple type of functionality which would result in different types of measurements for the controls effectiveness.  Careful consideration should be taken defining these terms so client messaging is not diluted.  Available functions for the control category will be mapped in the ControlCategory.  What functions are used for the control by the company will be mapped at the CompanyControl."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the controls function to support mitigation of the risk '),)  # Name of the control functionality
    description = models.TextField(
        blank=False, help_text=('Description of the control function'),)  # Name of the functionality description
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Keywords used to find the correct functionality.
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
        'Account', on_delete=models.PROTECT, related_name='account_controlfunction', help_text=('The account that the control function is related'),)  # Account associated with the control function.  Control fuctions belonging to core will be seen by all accounts.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Functions")


class ControlCategoryFunction(models.Model):
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


class ControlOperation(models.Model):
    """Control Operation.  This will determine the operating stage of the control to prevent risk.  Choices are preventive, detective, corrective, or predictive """

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the control operational level '),)  # Name of the control operational level
    description = models.TextField(
        blank=False, help_text=('Description of the operational level'),)  # The description of the control operational level.
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that the operational level should be in for form selection'),)  # Sort order for form selection.
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
        verbose_name_plural = ("Control Operation")


class ControlCategoryOperation(models.Model):
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


class ControlDomain(models.Model):
    """Control Domain.  This is the domain the control belongs."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the control domain'),)  # This is the name of the control domain.
    description = models.TextField(
        blank=False, help_text=('Description of the control domain'),)  # The description of the control domain.
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
        'Account', on_delete=models.PROTECT, related_name='account_controldomain', help_text=('The account that the control domain is related'),)  # Account associated with the control domain.  Control domains belonging to core will be seen by all accounts.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Domains")


class ControlCsc(models.Model):
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


class ControlCscFamily(models.Model):
    """Control CSC Family."""
    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the indicator'),)  # Not in use
    description = models.TextField(
        blank=True, null=True, help_text=('Description of the indicator'),)  # Not in use
    notes = models.TextField(
        blank=True, null=True,  help_text=('Notes associated wtih the indicator'),)  # Not in use
    example_title1 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 1'),)  # Not in use
    example_title2 = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Title used to support the example 2'),)  # Not in use
    example_content1 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 1'),)  # Not in use
    example_content2 = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Verbaige used to describe example 2'),)  # Not in use
    name = models.CharField(
        max_length=45, blank=False, help_text=('Family that the CSC belongs'),)  # Not in use
    description = models.TextField(
        blank=True, null=True, help_text=('Description of the family'),)  # Not in use
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control CSC Families")


class DependencyType(models.Model):
    """Dependency Type"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the dependencies effort'),)  # The name of the dependency type
    description = models.TextField(
        blank=False, help_text=('Description of the effort requried from the dependencies'),)  # Description of the dependency type.
    DEPENDENT_CHOICES = (
        ('contact', 'Contact'),
        ('team', 'Team'),
        ('vendor', 'Vendor'),
    )
    # Used to separate dependency types for select options for CompanyControl
    # m2m dependents.
    dependent = models.CharField(
        max_length=7, choices=DEPENDENT_CHOICES, default='CONTACT')
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

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Dependency Types")


class DependencyEffort(models.Model):
    """Future USE?  Dependency Effort.  This field is used to better describes the assocation the dependcy has with the control"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the dependencies effort'),)  # Not in use
    description = models.TextField(
        blank=False, help_text=('Description of the effort requried from the dependencies'),)  # Not in use
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed'),)  # Not in use
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
        verbose_name_plural = ("Dependency Efforts")
