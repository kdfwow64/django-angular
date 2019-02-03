"""Vendor, Product & related models."""
import datetime
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
    DefaultFieldsContext,
)


def current_year():
    return datetime.date.today().year

YEAR_CHOICES = []
for r in range(1900, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((r, r))


class Vendor(DefaultFieldsCompany):
    """Vendors for controls in place for the Company.  Most vendors will belong to Core Account and be used by all Companies, however companies can create their own vendors.  Those vendors will be under review to move to Core Account so all Companies can use them."""

    abbrv = models.CharField(
        max_length=10, blank=True, null=True, help_text=('Vendor abbreviated name'),)  # Abbrevation name
    about = models.TextField(
        blank=True, null=True, help_text=('Information about the vendor from their website'),)  # Information about the vendor
    year_established = models.IntegerField(
        help_text=('Year the vendor was established'), choices=YEAR_CHOICES, default='1900')  # Year the vendor was established
    phone_info = models.CharField(
        max_length=15, blank=True, null=True, help_text=('Vendor information phone number'),)  # General information for the vendor phone number
    phone_support = models.CharField(
        max_length=15, blank=True, null=True, help_text=('Vendor support phone number'),)  # Support phone number for the vendor
    email_info = models.EmailField(
        max_length=255, blank=True, null=True, help_text=('Addtional information email address for the vendor.'),)  # Email address should be unique for the vendor but sometimes they may duplicate due to aquistions.
    email_product = models.EmailField(
        max_length=255, blank=True, null=True, help_text=('For internal use to get information from the vendor regarding products and services'),)  # Email address should be unique for the vendor but sometimes they may duplicate due to aquistions.

    ''' Future usage for consistant updates on vendor url changes.
     import hashlib
     import urllib
     page = requests.get('<url>')
     hashlib.sha256(page.text.encode('utf-8')).hexdigest()
     req = urllib.request.Request('<url>')
     try: urllib.request.urlopen(req)
     except urllib.error.URLError as e:
      code=e.reason
    '''
    url_main_hash = models.CharField(
        max_length=256, blank=True, null=True, help_text=('Main url hash'),)  # Hashed website value for compare for changes
    url_contact_hash = models.CharField(
        max_length=256, blank=True, null=True, help_text=('Contact url hash'),)  # Hashed website value for compare for changes
    url_about_us_hash = models.CharField(
        max_length=256, blank=True, null=True, help_text=('About Us url hash'),)  # Hashed website value for compare for changes
    url_products_hash = models.CharField(
        max_length=256, blank=True, null=True, help_text=('Products url hash'),)  # Hashed website value for compare for changes
    url_services_hash = models.CharField(
        max_length=256, blank=True, null=True, help_text=('Services url hash'),)  # Hashed website value for compare for changes
    url_solutions_hash = models.CharField(
        max_length=256, blank=True, null=True, help_text=('Solutions url hash'),)  # Hashed website value for compare for changes
    url_main_http_code = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Main url http code'),)  # Last recorded HTTP code for the url
    url_contact_http_code = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Contact url http code'),)  # Last recorded HTTP code for the url
    url_about_us_http_code = models.CharField(
        max_length=5, blank=True, null=True, help_text=('About Us url http code'),)  # Last recorded HTTP code for the url
    url_products_http_code = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Products url http code'),)  # Last recorded HTTP code for the url
    url_services_http_code = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Services url http code'),)  # Last recorded HTTP code for the url
    url_solutions_http_code = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Solutions url http code'),)  # Last recorded HTTP code for the url
    url_main = models.URLField(max_length=200, blank=True, null=True, help_text=(
        'Vendors main website'),)  # Vendor website
    url_contact = models.URLField(max_length=200, blank=True, null=True, help_text=(
        'Vendors contact us website'),)  # Vendor website
    url_about_us = models.URLField(max_length=200, blank=True, null=True, help_text=(
        'Vendors about us website'),)  # Vendor website
    url_products = models.URLField(max_length=200, blank=True, null=True, help_text=(
        'Vendors products website'),)  # Vendor website
    url_services = models.URLField(max_length=200, blank=True, null=True, help_text=(
        'Vendors services website'),)  # Vendor website
    url_solutions = models.URLField(max_length=200, blank=True, null=True, help_text=(
        'Vendors solutions website'),)  # Vendor website
    url_crawler_days = models.IntegerField(blank=True, default=90,
                                           help_text=('Defines the default number of days a url scan should be performed'),)  # Default value should be set so to a value that does not insinuate a crawler and is frequent enough to catch vendor url changes.
    url_crawler_flg = models.BooleanField(
        default=False, help_text=('Defines if an url crawl is due for the vendor'),)  # If True, url crawl is needed.
    date_url_crawler = models.DateTimeField(null=True, blank=True, help_text=(
        'Timestamp the vendor url\'s were last crawlled'),)  # Timestamp the vendor url was last crawlled.
    name_aka = models.TextField(
        blank=True, null=True,  help_text=('Other names the company may have been associated'),)  # This field will be used for searching out a company.  Company's name may change for various reasons.
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
    stock_symbol = models.CharField(
        max_length=15, blank=True, null=True, help_text=('Vendor stock symbol'),)  # Used to trend vendor activity
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value that the vendor belongs too based on the company that owns the vendor.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the vendor'),)  # If True, evaluation is needed.
    date_evaluated = models.DateTimeField(null=True, blank=True, help_text=(
        'Timestamp the evaluation last occured'),)  # Date the user completed submitted the evaluation
    approved_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='%(app_label)s_%(class)s_related_approved', help_text=(
        'User id that approved the vendor'),)
    # Foreign Key and Relationships
    transitioned_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='transitioned_vendor', help_text=(
        'User id of the user that transitioned the vendor to CORE'),)  # User that transitioned the vendor to CORE.
    initial_account = models.ForeignKey('Account', default=1, on_delete=models.PROTECT, related_name='inital_account_vendor', help_text=(
        'Account that initally created the vendor'),)  # If an Account creates a vendor that is transitioned to CORE, this will keep track of the original account creator.
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
        return self.get_vendor_acronym()

    def get_vendor_acronym(self):
        """Get short name."""
        if self.abbrv:
            return "{} - {}".format(self.abbrv, self.name)
        else:
            return self.name
    get_vendor_acronym.short_description = 'Vendor with Acronym'


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
