"""Vendor, Product & related models."""
from django.db import models


class Vendor(models.Model):
    """Vendors for controls in place for the Company.  Most vendors will belong to Core Account and be used by all Companies, however companies can create their own vendors.  Those vendors will be under review to move to Core Account so all Companies can use them."""

    name = models.CharField(
        max_length=255, blank=False, help_text=('Vendor name'),)  # Name of the vendor
    parent = models.CharField(
        max_length=255, blank=True, help_text=('Vendor parent company'),)  # If a parent company is applicable
    abbrv = models.CharField(
        max_length=10, blank=True, help_text=('Vendor abbreviated name'),)  # Abbrevation name
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
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the vendor is active'),)  # Vendors may go out of business, merge, split, etc.
    under_review = models.BooleanField(
        default=False, help_text=('Designates whether the vendor is an organization'),)  # Vendors set to True are under review and should not be included in selections.
    review_reason = models.TextField(
        blank=True, null=True,  help_text=('Description of why the vendor is under review'),)  # Describe why the vendor is under review here.  This is for management purposes.
    date_transitioned = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the vendor was transitioned to CORE'),)  # Date the vendor was transitioned to CORE.  A review will need to take place.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the vendor was created'),)  # Date the vendor was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text=('Timestamp the vednor was modified'),)  # Date the vendor was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the vendor was deactivated'),)  # Date that the vendor was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the vendor was created'),)  # Date the vendor was deleted
    rank = models.IntegerField(
        default=0, blank=False, help_text=('Ranking of the vendor by the system'),)  # Used to rank vendors base on system logic.  This may be automated through the application.
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Keywords to find the vendor.  This should be updated based on control types
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
    transitioned_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='transitioned_vendor', help_text=(
        'User id of the user that transitioned the vendor to CORE'),)  # User that transitioned the vendor to CORE.
    created_by = models.ForeignKey('User', default=1, on_delete=models.PROTECT, null=True, related_name='created_vendor', help_text=(
        'User id of the user that created the field'),)  # User that created the vendor initally
    modified_by = models.ForeignKey('User', default=1, on_delete=models.PROTECT, null=True, related_name='modified_vendor', help_text=(
        'User id that last modified the field'),)  # User that last modified the vendor
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_vendor', help_text=(
        'User id if deactivated by another user.'),)  # User that deactivated the vendor
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deleted_vendor', help_text=(
        'User id if deleted by another user'),)  # User that deleted the vendor.  Note: Vendors are never deleted, just removed from view of the Account Users.
    initial_account = models.ForeignKey('Account', default=1, on_delete=models.PROTECT, related_name='inital_account_vendor', help_text=(
        'Acocunt that initally created the vendor'),)  # If an Account creates a vendor that is transitioned to CORE, this will keep track of the original account creator.
    account = models.ForeignKey('Account', default=1, on_delete=models.PROTECT, related_name='account_vendor', help_text=(
        'Account that the vendor is associated with.  If CORE, then all accounts'),)  # Vendors are defined at the Account level instead of the company level because Vendors chosen at the Account level will more than likely be used for multiple companies under the account.  When companies create Vendors, they will create them at the account level.
    vendortypes = models.ManyToManyField("VendorType", through='VendorTypeMap',
                                         through_fields=('vendor', 'vendor_type'), related_name='VendorTypeMapping', help_text=('Maps vendors to their associated type'),)  # Vendors may perform mupltiple type of functions for Accounts.
    vendorcategories = models.ManyToManyField("VendorCategory", through='VendorCategoryMap',
                                              through_fields=('vendor', 'vendor_category'), related_name='VendorTypeMapping', help_text=('Maps vendors to their associated category'),)  # Vendors may have multiple categorizations.

    def __str__(self):
        """String."""
        return self.name


class VendorType(models.Model):
    """VendorType."""
    name = models.CharField(
        max_length=100, blank=False, help_text=('Name of the vendor type'),)  # The type of vendor.
    desc = models.TextField(
        blank=True, help_text=('Decription of the vendor type'),)  # Descriptoin of the vendor type
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Keywords that would be used in searches to get to the vendor.
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
    account = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='account_vendortype', help_text=(
        'Acocunt that the vendortype is associated with.  If CORE, then all accounts'),)  # Vendors types are defined at the Account level instead of the company level because Vendors chosen at the Account level will more than likely be used for multiple companies under the account.  When companies create Vendor Types, they will create them at the account level.  The option to create a vendor type should only be available to Account Admin.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Vendor Types")


class VendorTypeMap(models.Model):
    """ Used to tie Vendors to the type of services they perform."""
    vendor = models.ForeignKey(
        'Vendor', on_delete=models.PROTECT)  # Vendor used from the vendor table
    # Vendor type used from the vendortype table.
    vendor_type = models.ForeignKey('VendorType', on_delete=models.PROTECT)
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the relationship is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not have access to the account.


class VendorCategory(models.Model):
    """Vendor Category.  Much like Gartners quadrents, but more detailed.  This helps companies find like products and services quickly."""

    name = models.CharField(
        max_length=100, blank=False, help_text=('Name of the vendor category'),)  # Name of the vendor category
    desc = models.TextField(
        blank=True, help_text=('Decription of the vendor category'),)  # Description of the vendor category
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Keywords used to find like vendors or the services/products sold.
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
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Description for quick hover.
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Description for form input.
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Vendor Categories")

    def __str__(self):
        """String."""
        return self.name


class VendorCategoryMap(models.Model):
    """ Used to tie Vendors to the type of categories they perform."""
    vendor = models.ForeignKey(
        'Vendor', on_delete=models.PROTECT)  # Vendor used from the vendor table
    # Vendor category used from the vendorcategory table.
    vendor_category = models.ForeignKey(
        'VendorCategory', on_delete=models.PROTECT)
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the relationship is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not have access to the account.
