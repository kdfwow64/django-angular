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
    url = models.URLField(max_length=200, blank=True, help_text=(
        'Url for the control'),)  # URL specific to the control defined.  Vendor URL's are in the model.
    name_aka = models.TextField(
        blank=True, null=True,  help_text=('Other names the control may have been associated'),)  # This field will be used for searching out controls.  A controls' name may change for various reasons.
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify or seach the field name'),)  # Keywords to find the control.  This should be updated based on control type
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=True, related_name='controldetail', help_text=(
        'Vendor that produces the control '),)  # Vendor that makes or maintains the control.  If the account manages/creates the control then this should be listed as Self.
    onus_method = models.ManyToManyField("OnusMethod", through='ControlOnusMethod', through_fields=('id_control', 'id_onus_method'), related_name='controlonusmethods', help_text=(
        'Who owns the burden of responsibility to produce value from the control'),)  # This will help users of the application seperate DIY (do it yourself), DIFY (do it for you), DIWY (do it with you).
    delivery_method = models.ManyToManyField("DeliveryMethod", through='ControlDeliveryMethod', through_fields=('id_control', 'id_delivery_method'), related_name='controldeliverymethods', help_text=(
        'In what form is the control provided for use'),)  # This will help users of the application understand the way the logic is provided to them and what additional dependencies are needed to suppport it.
    billing_method = models.ManyToManyField("BillingMethod", through='ControlBillingMethod', through_fields=('id_control', 'id_billing_method'), related_name='controlbillingmethods', help_text=(
        'How is the control purchased'),)  # This will help users of the application understand how the control should be budgeted.
    categories = models.ManyToManyField("ControlCategory", through='ControlCategoryControl', through_fields=('id_control', 'id_controlcategory'), related_name='controlcategory_controlcategor', help_text=(
        'The protection categories that the control provides'),)  # Used to categorize the protection the control performs

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Controls")


class ControlCategoryControl(DefaultFields):
    """Through model for Control.  Used determine what type of protection the control provides"""

    # Foreign Key and Relationships
    id_control = models.ForeignKey('Control', on_delete=models.PROTECT, null=True, related_name='controlcategory_control', help_text=(
        'The control'),)
    id_controlcategory = models.ForeignKey('ControlCategory', on_delete=models.PROTECT, null=True, related_name='control_controlcategory', help_text=(
        'Category of control'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Control Categories")

    def __str__(self):
        return self.id_controlcategory.name


class ControlCategory(DefaultFieldsCategory):
    """Control Category."""

    control_category_type = models.ForeignKey('ControlCategoryType', on_delete=models.PROTECT, null=True, related_name='type_controlcategory', help_text=(
        'Type of control category'),)
    control_domain = models.ForeignKey('ControlDomain', on_delete=models.PROTECT, null=True, related_name='category_controldomain', help_text=(
        'Type of control category domain'),)
    control_family = models.ForeignKey('ControlFamily', on_delete=models.PROTECT, null=True, related_name='category_controlfamily', help_text=(
        'Family that the control category belongs'),)
    control_response = models.ManyToManyField("ControlResponse", through='ControlCategoryResponse', through_fields=('id_controlcategory', 'id_controlresponse'), related_name='ControlResponseLevel', help_text=(
        'The level at which the control category alerts to repsonder'),)  # Control categories can have multiple operation levels.  This field is used show what may be available for the control.
    core_expectation = models.TextField(
        blank=True, null=True, help_text=('Description of the primary purpose of the control.'),)  # This field will help the user better how to measure value of the control.
    control_function = models.ManyToManyField("ControlFunction", through='ControlCategoryFunction', through_fields=('id_controlcategory', 'id_controlfunction'), related_name='ControlFunctions', help_text=(
        'The level at which the control category functions'),)  # Control categories can have multiple functions that they perform for the business.  This field is used show what may be available for the control.
    control_feature = models.ManyToManyField("ControlFeature", through='ControlCategoryFeature', through_fields=('id_controlcategory', 'id_controlfeature'), related_name='ControlCategoryFeatures', help_text=(
        'The level at which the control category features'),)  # Control categories can have multiple features that they perform for the business.  This field is used show what may be available for the control.
    cia_triad = models.ManyToManyField('CIATriad', through='ControlCategoryCIATriad', through_fields=('id_controlcategory', 'id_ciatriad'), related_name='ControlCategoryCIATriads', help_text=(
        'Specifies what portion of the triad is associated to the control category'),)  # Ties CIA Triad to the event entry.

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


class ControlCategoryCIATriad(DefaultFields):
    """Through model for Control Category.  Define the triad to the control category"""

    id_controlcategory = models.ForeignKey('ControlCategory', on_delete=models.PROTECT, null=True, related_name='cia_controlcategory', help_text=(
        'The control category the associated with the CIA Triad'),)
    id_ciatriad = models.ForeignKey('CIATriad', on_delete=models.PROTECT, null=True, related_name='controlcategory_cia', help_text=(
        'The CIA Triad'),)
    context = models.TextField(
        blank=True, help_text=('Context regarding the CIA triad'),)  # Additional information on why the triad is associated to the eventtype.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Category: CIA Triad")


class ControlResponse(DefaultFieldsCategory):
    """Control Response.  This will determine the operating stage of the control to prevent risk.  Choices are preventive, detective, corrective, or predictive """

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Responses")
        ordering = ['sort_order', ]


class ControlCategoryResponse(DefaultFields):
    """Control Category Operation.  Used to define what operation levels are availabe for the user to chose"""

    # Foreign Key and Relationships
    id_controlcategory = models.ForeignKey('ControlCategory', on_delete=models.PROTECT, null=True, related_name='category_control_response', help_text=(
        'Category of control'),)
    id_controlresponse = models.ForeignKey('ControlResponse', on_delete=models.PROTECT, null=True, related_name='response_control_category', help_text=(
        'Type of notification response the control provides.'),)
    description = models.TextField(
        blank=False, help_text=('Description of the how the control would operate at the selected level'),)  # This field will help the user better understand how they are using the control defined.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Category: Notification Types")


class ControlFunction(DefaultFieldsCategory):
    """Control Funtion.  This will determine what the contorl type does.  What function does in play in mitigating the risk for the business """

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Functions")
        ordering = ['sort_order', ]


class ControlCategoryFunction(DefaultFields):
    """Control Category Function.  Used to define what functions are availabe for the user to chose for the control type"""

    # Foreign Key and Relationships
    id_controlcategory = models.ForeignKey('ControlCategory', on_delete=models.PROTECT, null=True, related_name='category_control_function', help_text=(
        'Category of control'),)
    id_controlfunction = models.ForeignKey('ControlFunction', on_delete=models.PROTECT, null=True, related_name='function_control_category', help_text=(
        'Type of function the control provides.'),)
    description = models.TextField(
        blank=False, help_text=('Description of the how the control would function at the selected level'),)  # This field will help the user better understand how they are using the control defined.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Category Function Map")


class ControlFeature(DefaultFieldsCategory):
    """Control Feature.  This will determine what the control type does.   """

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Features")
        ordering = ['sort_order', ]


class ControlCategoryFeature(DefaultFields):
    """Control Category Feature.  Used to define what features are available for the control category"""

    # Foreign Key and Relationships
    id_controlcategory = models.ForeignKey('ControlCategory', on_delete=models.PROTECT, null=True, related_name='category_control_feature', help_text=(
        'Category of control'),)
    id_controlfeature = models.ForeignKey('ControlFeature', on_delete=models.PROTECT, null=True, related_name='feature_control_category', help_text=(
        'Type of feature the control provides.'),)
    is_key = models.BooleanField(
        default=False, help_text=('Defines feature should be considered a key feature'),)  # Used to highlight the key features of the control.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control Category Feature Map")


class ControlDomain(DefaultFieldsCategory):
    """Control Domain.  This is the domain the control belongs."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Domains")


class ControlFamily(DefaultFieldsCategory):
    """Control Family.  This should be the highest level a control cateogry can belong too."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Families")


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
        verbose_name_plural = ("Control: CSC")


class ControlCscFamily(DefaultFieldsCompany):
    """Control CSC Family."""
    notes = models.TextField(
        blank=True, null=True,  help_text=('Notes associated wtih the indicator'),)  # Not in use

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: CSC Families")


class ControlOnusMethod(DefaultFields):
    """Control - Onus Method Through Model."""

    # Foreign Key and Relationships
    id_control = models.ForeignKey('Control', on_delete=models.PROTECT, null=True, related_name='control_onus_method', help_text=(
        'Name of the control'),)
    id_onus_method = models.ForeignKey('OnusMethod', on_delete=models.PROTECT, null=True, related_name='onus_method_control', help_text=(
        'Method of client onus.'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Onus Methods Map")


class ControlDeliveryMethod(DefaultFields):
    """Control - Delivery Method Through Model."""

    # Foreign Key and Relationships
    id_control = models.ForeignKey('Control', on_delete=models.PROTECT, null=True, related_name='control_delivery_method', help_text=(
        'Name of the control'),)
    id_delivery_method = models.ForeignKey('DeliveryMethod', on_delete=models.PROTECT, null=True, related_name='delivery_method_control', help_text=(
        'Method of vendor delivery.'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Delivery Methods Map")


class ControlBillingMethod(DefaultFields):
    """Control - Billing Method Through Model."""

    # Foreign Key and Relationships
    id_control = models.ForeignKey('Control', on_delete=models.PROTECT, null=True, related_name='control_billing_method', help_text=(
        'Name of the control'),)
    id_billing_method = models.ForeignKey('BillingMethod', on_delete=models.PROTECT, null=True, related_name='billing_method_control', help_text=(
        'Method of billing.'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Billing Methods Map")


class OnusMethod(DefaultFieldsCategory):
    """Widget Type."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Onus Methods")


class DeliveryMethod(DefaultFieldsCategory):
    """Widget Type."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Delivery Methods")


class BillingMethod(DefaultFieldsCategory):
    """Widget Type."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Control: Billing Methods")


class DependencyEffort(DefaultFieldsCompany):
    """Future USE?  Dependency Effort.  This field is used to better describes the assocation the dependcy has with the control"""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Dependency Efforts")
