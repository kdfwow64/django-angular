"""Vendor, Product & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
)


class Vendor(DefaultFieldsCompany):
    """Vendors for controls in place for the Company.  Most vendors will belong to Core Account and be used by all Companies, however companies can create their own vendors.  Those vendors will be under review to move to Core Account so all Companies can use them."""

    abbrv = models.CharField(
        max_length=10, blank=True, null=True, help_text=('Vendor abbreviated name'),)  # Abbrevation name
    about = models.TextField(
        blank=True, help_text=('Information about the vendor from their website'),)  # Information about the vendor
    notes_mgmt = models.TextField(
        blank=True, help_text=('Management notes regarding the vendor'),)  # Management notes about the vendor
    phone_info = models.CharField(
        max_length=15, blank=True, help_text=('Vendor information phone number'),)  # General information for the vendor phone number
    phone_support = models.CharField(
        max_length=15, blank=True, help_text=('Vendor support phone number'),)  # Support phone number for the vendor
    url_main = models.URLField(max_length=200, blank=True, help_text=(
        'Vendors main website'),)  # Vendor website
    url_product = models.URLField(max_length=200, blank=True, help_text=(
        'Vendors products website'),)  # Vendor website
    url_service = models.URLField(max_length=200, blank=True, help_text=(
        'Vendors services website'),)  # Vendor website
    url_support = models.URLField(max_length=200, blank=True, help_text=(
        'Vendors support website'),)  # Vendor website
    under_review = models.BooleanField(
        default=False, help_text=('Designates whether the vendor is an organization'),)  # Vendors set to True are under review and should not be included in selections.
    review_reason = models.TextField(
        blank=True, null=True,  help_text=('Description of why the vendor is under review'),)  # Describe why the vendor is under review here.  This is for management purposes.
    date_transitioned = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the vendor was transitioned to CORE'),)  # Date the vendor was transitioned to CORE.  A review will need to take place.
    rank = models.IntegerField(
        default=0, blank=False, help_text=('Ranking of the vendor by the system'),)  # Used to rank vendors base on system logic.  This may be automated through the application.
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Keywords to find the vendor.  This should be updated based on control types
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value that the vendor belongs too based on the company that owns the vendor.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the vendor'),)  # If True, evaluation is needed.
    account_approved = models.BooleanField(
        default=False, help_text=('Defines if a company vendor can be used at the account level'),)  # If True, all companies under the account can leverage the vendor, if False only the company that added the vendor can leverage them.
    # Foreign Key and Relationships
    transitioned_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='transitioned_vendor', help_text=(
        'User id of the user that transitioned the vendor to CORE'),)  # User that transitioned the vendor to CORE.
    initial_account = models.ForeignKey('Account', default=1, on_delete=models.PROTECT, related_name='inital_account_vendor', help_text=(
        'Acocunt that initally created the vendor'),)  # If an Account creates a vendor that is transitioned to CORE, this will keep track of the original account creator.
    parent = models.ForeignKey('Vendor', blank=True, null=True, on_delete=models.PROTECT, related_name='parent_vendor', help_text=(
        'Parent company of the vendor'),)  # The parent company of the vendor.  If none, then it is the parent
    # Vendors are defined at the Company level need to be approved by the
    # option Vendor.account_approved at the account level for before other
    # companies in the same account can leverage the vendor.
    vendortypes = models.ManyToManyField("VendorType", through='VendorTypeMap',
                                         through_fields=('id_vendor', 'id_vendortype'), related_name='vendortype_mapping', help_text=('Maps vendors to their associated type'),)  # Vendors may perform mupltiple type of functions for Accounts.
    vendorcategories = models.ManyToManyField("VendorCategory", through='VendorCategoryMap',
                                              through_fields=('id_vendor', 'id_vendorcategory'), related_name='vendorcategory_mapping', help_text=('Maps vendors to their associated category'),)  # Vendors may have multiple categorizations.

    def __str__(self):
        """String."""
        return self.name


class VendorType(DefaultFieldsCategory):
    """VendorType."""

    class Meta:
        """Meta class."""
        ordering = ('name',)
        verbose_name_plural = ("Vendor Types")

    def __str__(self):
        """String."""
        return self.name


class VendorTypeMap(DefaultFields):
    """ Through table for Vendor Used to tie Vendors to the type of services they perform."""
    id_vendor = models.ForeignKey(
        'Vendor', on_delete=models.PROTECT)  # Vendor used from the vendor table
    # Vendor type used from the vendortype table.
    id_vendortype = models.ForeignKey(
        'VendorType', on_delete=models.PROTECT)


class VendorCategory(DefaultFieldsCategory):
    """Vendor Category.  Much like Gartners quadrents, but more detailed.  This helps companies find like products and services quickly."""

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Vendor Categories")

    def __str__(self):
        """String."""
        return self.name


class VendorCategoryMap(DefaultFields):
    """ Used to tie Vendors to the type of categories they perform."""
    id_vendor = models.ForeignKey(
        'Vendor', on_delete=models.PROTECT)  # Vendor used from the vendor table
    # Vendor category used from the vendorcategory table.
    id_vendorcategory = models.ForeignKey(
        'VendorCategory', on_delete=models.PROTECT)
