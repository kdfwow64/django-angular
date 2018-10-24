"""Company & related models."""
from django.db import models
from risk.models.auth import User, UserGrant


class Company(models.Model):
    """Company."""

    about = models.TextField(blank=True, help_text=(
        'About the company'),)  # About the company.  This helps to better understand the company.
    url = models.URLField(max_length=200, blank=True, help_text=(
        'Company website'),)  # URL for the company
    name = models.CharField(
        max_length=128, blank=False, help_text=('Company name'),)  # Name of the company.  This will also default the account name if it is the first company created under an account without a name.  Admin can modify the company name.
    fixed_max_loss = models.DecimalField(default=0, blank=True, max_digits=30, decimal_places=2, help_text=(
        'Maximum fixed monetary loss the company can sustain'),)  # This is fixed cost of the maximum amount of annual monetary loss a company can sustain without going bankrupt.  Monetary_value_toggle = False.  Used determine logic regarding impact and cost.  This value can be greater than annual revenue
    par_max_loss = models.FloatField(default=0, blank=True, help_text=(
        'Maximum percentage of annual revenue loss the company can sustain'),)  # This is the percentage of annual revenue loss a company can sustain without going bankrupt.  Monetary_value_toggle = True.  Used determine logic regarding impact and cost.  This value can be greater than annual revenue
    monetary_value_toggle = models.BooleanField(
        default=False, help_text=('Toggle to determine if company max loss is measured by fixed=False or par =True monetary value'),)  # If False, use Fixed Loss for calculations.  If True, use PAR loss for calculations.
    annual_revenue = models.DecimalField(blank=True, default=0, max_digits=30, decimal_places=2, help_text=(
        'Annual revenue of the company. Requred if the toggle is set to par_max_loss'),)  # Annual revenue of the company.  Carried to 2 decimal places in case this is written via API from other system.
    weight_frequency = models.FloatField(default=1, help_text=(
        'Company specific weighted value for frequency'),)  # In special cases based on the type of business.  The frequency weight may need to be adjusted.
    weight_impact = models.FloatField(default=1, help_text=(
        'Company specific weighted value for impact'),)  # In special cases based on the type of business the impact weight may need to be adjusted.  Defaults to a 1 multiplier
    weight_severity = models.FloatField(default=1, help_text=(
        'Company specific weighted value for severity'),)  # In special cases based on the type of business the severity weight may need to be adjusted.  Defaults to a 1 multiplier
    resilience_max = models.IntegerField(blank=True, null=True, help_text=(
        'Maximum number of units any control have to recover'),)  # Resilience time is used to determine if there are controls that may not recover in an appropirate time frame.
    company_notes = models.TextField(
        blank=True, null=True, help_text=('Company notes that the contriburtor can add'),)  # Notes about the company.  This field is mainly used if the account is a reseller or using the tool for mulitple business units.
    evaluation_days = models.IntegerField(
        default=365, help_text=('Defines the default number of days an evaluation should occur'),)  # Used to define the default value for all evaluation timeframes.  If no evaluations are requested, this should be set to 0.  Note:  For models that need to be evaluated such as Entries, Controls, Assets, Vendors, Individuals, etc. there is an evaluation_flg that can be set and will overide the date range.
    evaluation_alert_days = models.IntegerField(
        default=14, blank=False, help_text=('Range in days that an alert should be sent the evaluation is due'),)  # Used to trigger an alert that the evaluation period is coming.
    defined1_data_entry_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined1 data field name for the entry table'),)  # Not in use
    defined2_data_entry_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined2 data field name for the entry table'),)  # Not in use
    date_defined1_entry_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined1 date field name for the entry table'),)  # Not in use
    date_defined2_entry_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined2 date field name for the entry table'),)  # Not in use
    defined1_data_dependency_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined1 data field name for the dependency table'),)  # Not in use
    defined2_data_dependency_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined2 data field name for the dependency table'),)  # Not in use
    date_defined1_dependency_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined1 date field name for the dependency table'),)  # Not in use
    date_defined2_dependency_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined2 date field name for the dependency table'),)  # Not in use
    defined1_data_individual_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined1 data field name for the individual table'),)  # Not in use
    defined2_data_individual_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined2 data field name for the individual table'),)  # Not in use
    date_defined1_individual_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined1 date field name for the individual table'),)  # Not in use
    date_defined2_individual_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined2 date field name for the individual table'),)  # Not in use
    defined1_data_individual_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined1 data field name for the individual table'),)  # Not in use
    defined2_data_individual_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined2 data field name for the individual table'),)  # Not in use
    date_defined1_individual_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined1 date field name for the individual table'),)  # Not in use
    date_defined2_individual_label = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the custom defined2 date field name for the individual table'),)  # Not in use
    """Application Input"""
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this company should be treated as active'),)  # Determines if the company is active
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the deactivated the company'),)  # Date that the company was deactivated
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Timestamp the company was created'),)  # Date that the company was created
    date_modified = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Timestamp the company was modified'),)  # Last date the company record was modified
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the company was created'),)  # Date that the company was deleted by the Account Admin.  Note: Company will not be permenantly deleted.  It will not be viewable to the Account users.
    utility_field = models.CharField(
        max_length=30, blank=True, help_text=('Backoffice field used for queries and reporting'),)  # This field is not viewable to the Account users and is used for backoffice reporting and testing.
    bkof_notes = models.TextField(
        blank=True, help_text=('Backoffice notes on company'),)  # This field is not viewable to the Account users and is use for backoffice detail only.
    created_by = models.ForeignKey('User', on_delete=models.PROTECT,  null=True, blank=True, related_name='created_company', help_text=(
        'User id if created by another user'),)  # User that created the company
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='modified_company', help_text=(
        'User id if created by another user'),)  # User that last modfied the company record
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='deactivated_company', help_text=(
        'User id if deactivated by another user'),)  # User that deactivated the company
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='deleted_company', help_text=(
        'User id if deleted by another user'),)   # User that deleted the company.  Note: Company will not be permenantly deleted.  It will not be viewable to the Account users.
    account = models.ForeignKey('Account', on_delete=models.PROTECT, blank=False, related_name='account_company', help_text=(
        'The account the company was created under'),)  # The account the company was created from.
    naics = models.ForeignKey('Naics', on_delete=models.PROTECT, null=True, blank=True, related_name='naics_company', help_text=(
        'The NAICS code the defines the clients vertical / industry'),)  # The NAICS code for the company.  This is important for vertical reporting.  Account Admin should be able leverage a search function to determine the companies NAICS from the company profile page.
    resilience_unit = models.ForeignKey(
        'TimeUnit', on_delete=models.PROTECT, default=3, null=True, related_name='maxresilienceunit', help_text=('Resilience time unit of the company control'),)  # This setting combined with resilience_max will define the maximum time it should take to recover any control.
    currencytype = models.ForeignKey('CurrencyType', on_delete=models.PROTECT, default=1, blank=False, related_name='currencytype_company', help_text=(
        'Type of currency the company uses for financing'),)  # This will be used to determine the type of currency a company will leverage for the tool.  It should be determined before the cost loss is generated.  Monetary value logic will need to created based off this setting.  USD by default.
    user_member = models.ManyToManyField('User', through='CompanyMember',
                                         through_fields=('id_company', 'id_user'), related_name='CompanyUserMembers', help_text=('Specifies what users have access to the company'),)  # Specifies what users have acess to the company.

    class Meta:
        """Meta class."""

        ordering = ['account']
        indexes = [
            models.Index(fields=['name'], name='name_idx'), ]
        verbose_name_plural = ("Companies")

    def __str__(self):
        """String."""
        return self.name

    def get_active_register(self):
        """Get active register for this company."""
        # Return first for timebeing.
        return self.company_register.first()


class CompanyProfile(models.Model):
    """
    Company profilfe detail to gain a good understanding of the client.  This is separate from the company model because it is focused on the how the company operates.
    """

    company = models.OneToOneField(
        Company, on_delete=models.PROTECT,)
    sales_margin = models.TextField(
        blank=True, null=True, help_text=('Brief description how the company dictates margins'),)  # This helps define the expecation for margins on products and services.
    target_audience = models.TextField(
        blank=True, null=True, help_text=('Brief description who the target audience is in the company'),)  # This helps define who is likely to purchase products and services.
    value_statement = models.TextField(
        blank=True, null=True, help_text=('Brief description how the company defines value of products/services'),)  # This helps define why the product would be purchased
    culture_perception = models.TextField(
        blank=True, null=True, help_text=('Brief description how the company culture is percieved'),)  # This helps define perception of the company culture.
    number_employees = models.IntegerField(
        blank=True, null=True, help_text=('The number of employees in the company'),)  # Number of employees in the company.
    number_customers = models.IntegerField(
        blank=True, null=True, help_text=('The number of customers the company services'),)  # Number of customers the company.
    historical_growth_rate = models.FloatField(
        blank=True, null=True, help_text=('Historical Year-over-Year Growth Rate'),)  # Used to determine how quickly the company is growing.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Profiles")

    def __str__(self):
        """String representation."""
        return str(self.company.name)


class CompanyMember(models.Model):
    ''' This table is used to tie users to a specific company.  '''
    id_user = models.ForeignKey(
        'User', on_delete=models.PROTECT)  # User Id from the User table
    # Company Id from the Company table
    id_company = models.ForeignKey('Company', on_delete=models.PROTECT)
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company user grant relationship is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not have grant on the company.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Date the company grant was applied'),)  # Not in use
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='UserCreatedGrant', help_text=(
        'User id of the user that created the access'),)
    date_revoked = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the company grant was revoked, if applicable'),)  # Date company grant was revoked.
    revoked_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='UserRevokedGrant', help_text=(
        'User id if revoked by another user'),)  # User id of the admin that revoked the company grant
    user_grants = models.ManyToManyField("UserGrant", through='CompanyMemberGrant',
                                         through_fields=('id_companymember', 'id_usergrant'), related_name='CompanyMemberGrants', help_text=('Specifies what users have access to the company'),)  # Specifies what users have acess to the company.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Members")
        ordering = ('id_company',)

    def __str__(self):
        """String."""
        # return self.id_companymember
        return self.id_company.name + " - " + self.id_user.full_name


class CompanyMemberGrant(models.Model):
    """Company Member Grant."""

    # Foreign Key and Relationships
    id_companymember = models.ForeignKey('CompanyMember', on_delete=models.PROTECT, related_name='grant_companymember', help_text=(
        'The company member that gets a grant'),)  # Id of the company member
    id_usergrant = models.ForeignKey('UserGrant', on_delete=models.PROTECT, related_name='member_usergrant', help_text=(
        'The grant assigned to the company member'),)  # Id of the grant assigned to the company member.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the grant for the member is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the grant will not be active for the user.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Member Grants")

    def __str__(self):
        """String."""
        # return self.id_companymember
        return self.id_companymember


class CompanyMemberRole(models.Model):
    """ The role the member plays in the company."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Role of the member'),)  # Role of the member
    description = models.TextField(
        blank=True, null=True, help_text=('Description of the role'),)  # Role description of the member
    keywords = models.TextField(
        blank=True, help_text=('Words used to search the role'),)  # Role description of the member
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the role is active for use'),)
    company_member_role_type = models.ForeignKey(
        'CompanyMemberRoleType', blank=True, null=True, related_name='company_memberroletype', on_delete=models.PROTECT, help_text=('The role type that the member role is related'),)  # The type of role the member belongs to.
    company = models.ForeignKey(
        'Company', default=1, related_name='company_memberrole', on_delete=models.PROTECT, help_text=('The company that the member role is related'),)  # Companies have the ability to add their own member roles if desired.  These will be under review for addtion to CORE.  Default submission is set to Core Company.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Member Roles")


class CompanyMemberRoleType(models.Model):
    """ The type of role of the company member"""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the company role type'),)  # Role type name
    description = models.TextField(
        blank=True, null=True, help_text=('Description of the company role type'),)  # Role type description
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the role is active for use'),)
    company = models.ForeignKey(
        'Company', default=1, related_name='company_roletype', on_delete=models.PROTECT, help_text=('The company that the role type is managed.'),)  # Companies have the ability to add their own role types if desired.  These will be under review for addtion to CORE.  Default submission is set to Core Company.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Member Role Types")


class CompanyAsset(models.Model):
    """Company Asset.

    This allows the company to add multiple asset types to their register
    entries.  Companies will define the asset then determine what type of asset it is, along with the ability to group assets for reporting
    """
    STATUS_CHOICES = (
        (1, 'Fixed Value'),
        (2, 'Percent of Revenue'),
        (3, 'Time Based Value'),
    )  # Define which logic to use when generating asset value against the entry threat scenario.
    name = models.CharField(
        max_length=100, blank=False, help_text=('Name of the company asset'),)  # Company to determine the name of the asset
    notes = models.TextField(
        blank=True, help_text=('Notes about the company asset'),)  # Notes regarding the asset
    asset_value_fixed = models.DecimalField(blank=True, null=True, max_digits=30, decimal_places=2, help_text=(
        'The fixed monetary value of the asset in dollars'),)  # Asset value may be a fixed cost if monetary_value_toggle is set to False.
    asset_quantity_fixed = models.IntegerField(
        default=1, blank=False, help_text=('The quantity of fixed_monetary_value'),)  # This will be multipled by the fixed_monetary_value to get a total value of the asset(s) defined.
    asset_value_par = models.FloatField(blank=True, null=True, help_text=(
        'The percentage of monetary value of the asset to the annual revenue'),)  # Asset value may be a percentage of annual revenue if monetary_value_toggle is set to True.
    asset_value_timed = models.DecimalField(blank=True, null=True, max_digits=30, decimal_places=2, help_text=(
        'The monetary value of the asset per unit of time'),)  # The monetary value for the unit of time chosen
    asset_timed_quantity_relative = models.FloatField(blank=True, null=True, help_text=(
        'Number of time units to be used from the avaliable pool'),)  # Based-off the asset_timed_quantity_avaliable, this is the amount of time that is relative to the asset to be used in the entry.  This value may represent a more realistic value based on the environment.  This value cannot exceed the quantity_avaliable value.
    asset_timed_quantity_avaliable = models.FloatField(blank=True, null=True, help_text=(
        'The amount of time units avaiable annually'),)  # This will be used to determine available pool of time units in a year.  This value cannot exceed the annual value  of the time unit in the time units model.
    asset_value_toggle = models.IntegerField(choices=STATUS_CHOICES, default=1,
                                             help_text=('Toggle to determine which formula is used to determine the assets value'),)  # This toggle defaults to '1' a fixed value.
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the asset'),)  # If True, evaluation is needed.
    """Application Input"""
    # Foreign Key and Relationships
    asset_timed_unit = models.ForeignKey(
        'TimeUnit', on_delete=models.PROTECT, default=3, null=True, related_name='companyassetunits', help_text=('Time units used to determine the value of the asset'),)  # This setting combined with the relative quantitiy and asset value will define the cost of the asset.  Default "3" is set to hours as the unit of time.
    asset_owner = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='companycontact_asset', help_text=(
        ' Who owns the the information'),)  # If you own the information, you own the risk.
    company = models.ForeignKey('Company', on_delete=models.PROTECT, blank=False, related_name='companyassets', help_text=(
        'Company id for the company that was changed'),)  # Company that defined the asset
    asset_type = models.ForeignKey('CompanyAssetType', on_delete=models.PROTECT, blank=False, related_name='companyassettype', help_text=(
        'Type of asset being specified'),)  # The type of asset that was defined by CORE
    company_locations = models.ManyToManyField('CompanyLocation', blank=True, through='CompanyAssetLocation', through_fields=(
        'id_companyasset', 'id_companylocation'), related_name='CompanyAssetLocation', help_text=('Specified geo locations for the company'),)  # Locations of the company asset. If 1 then ALL assets.
    company_segments = models.ManyToManyField("CompanySegment", blank=True, through='CompanyAssetSegment', through_fields=(
        'id_companyasset', 'id_companysegment'), related_name='CompanyAssetSegment', help_text=('Specified logical segments for the company'),)  # Segments of the company control. If 1 then ALL segments.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Assets")

    def get_asset_value(self):
        if asset_value_toggle == 1:
            # Fixed - The asset value has a fixed cost.  Total value may
            # flucuate based on quantity
            return (self.asset_value_fixed * self.asset_quantity_fixed)
        elif asset_value_toggle == 2:
            # PAR -  The asset value is based on a percentage of revenue for
            # the company
            return (self.asset_value_par * self.id_company.annual_revenue)
        elif asset_value_toggle == 3:
            # Time based  - The asset has a time based value.  The contributor
            # must determine what is relative.
            return (self.asset_value_timed * self.asset_timed_quantity_relative)


class CompanyAssetType(models.Model):
    """
    Asset Type.

    Assets may come in many types both tangable (physical device)and
    intangable (business process).  This table describes the asset type.
    """

    name = models.CharField(
        max_length=30, help_text=('Type of asset'),)  # Not in use
    description = models.TextField(
        blank=False, help_text=('Description of the asset'),)  # Not in use
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
    company = models.ForeignKey('Company', default=1, on_delete=models.PROTECT, blank=False, related_name='companyassettype', help_text=(
        'Company id for the company that created the assettype'),)  # Company that defined the asset.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Asset Types")


class CompanyAssetSegment(models.Model):
    """Company Asset Segment."""

    # Foreign Key and Relationships
    id_companyasset = models.ForeignKey('CompanyAsset', on_delete=models.PROTECT, related_name='asset_companysegment', help_text=(
        'The company and asset'),)  # Id of the company control
    id_companysegment = models.ForeignKey('CompanySegment', on_delete=models.PROTECT, related_name='segment_companyasset', help_text=(
        'The company segment that the asset is used'),)  # Id of the company segment.  If 1 is used, this means All locations.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company asset segment is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not be able to select the asset segment.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Asset Segments")


class CompanyAssetLocation(models.Model):
    """Company Asset Location."""

    # Foreign Key and Relationships
    id_companyasset = models.ForeignKey('CompanyAsset', on_delete=models.PROTECT, related_name='asset_companylocation', help_text=(
        'The company and control'),)  # Id of the company control
    id_companylocation = models.ForeignKey('CompanyLocation', on_delete=models.PROTECT, related_name='location_companyasset', help_text=(
        'The company location that the asset is located'),)  # Id of the company location.  If 1 is used, this means All locations.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company asset location is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not be able to select the asset location.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Asset Locations")


class CompanyControl(models.Model):
    """Company Control.  This table will tie companies to the available controls in the Control table"""

    name = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Name of the control details'),)  # Name of the company control. This maybe use to better describe the use of the control.  Companies may opt to segment controls of the same type, location, etc.  This allow for that ability.
    description = models.TextField(
        blank=True, null=True, help_text=('Description of the control detail'),)  # Description of the company control.
    abbrv = models.CharField(
        max_length=30, blank=True, help_text=('Abbreviation of the name'),)  # Abbreviation of the company control.  Will be used in reporting if present.
    alias = models.CharField(
        max_length=128, blank=True, help_text=('Control alias'),)  # Alias used for the company control.  Will be used for reporting if present.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company control is active'),)  # The only active controls should be viewed by Account Users.
    version = models.CharField(
        max_length=100, blank=True, help_text=('Current control version'),)  # Version used for the company control.  Could be policy version, release version,etc It depends on the control defined.
    avg_annual_upkeep = models.DecimalField(default=0, blank=True, max_digits=30, decimal_places=2, help_text=(
        'Annual cost for licensing, etc. (-dependencies)'),)  # Normally 18% of capital expendure if applicable.  Control costs are captured in the CompanyControlCost table, this field is used for future projections.
    date_maint = models.DateField(null=True, blank=True, help_text=(
        'Annual maintenance date'),)  # Used to determine annual date that maintenance is completed for the control.
    centralized = models.BooleanField(default=True, help_text=(
        'Is the company control centralized or decentralized'),)  # If True, the control is a centralized control.  If False, the control is decentralized.
    budgeted = models.BooleanField(default=True, help_text=(
        'The control is currently budgeted'),)  # Not in use
    recovery_integer = models.FloatField(blank=True, null=True, help_text=(
        'Number of units it takes the control to recover'),)  # This setting combined with the resilience_unit will define the time required to get the control back to an operational state.
    recovery_time_unit = models.ForeignKey(
        'TimeUnit', on_delete=models.PROTECT, default=3, null=True, related_name='controlresilienceunites', help_text=('Resilience time unit of the company control'),)  # This setting combined with resilience_number will define the time it takes for a control to recover.
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the control'),)  # If True, evaluation is needed.
    defined1_data = models.CharField(max_length=128, blank=True, help_text=(
        'Custom company field for company control table -see company table'),)  # Not in use
    date_defined1 = models.DateTimeField(null=True, blank=True, help_text=(
        'Custom company field for company control table -see company table'),)  # Not in use
    defined2_data = models.CharField(max_length=128, blank=True, help_text=(
        'Custom company field for company control table -see company table'),)  # Not in use
    date_defined2 = models.DateTimeField(null=True, blank=True, help_text=(
        'Custom company field for company control table -see company table'),)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Date the company grant was applied'),)  # Not in use
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='UserCreatedCompanyControl', help_text=(
        'User id of the user that created the access'),)
    date_revoked = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the company grant was revoked, if applicable'),)  # Date company grant was revoked.
    revoked_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='UserRevokedCompanyControl', help_text=(
        'User id if revoked by another user'),)  # User id of the admin that revoked the company grant
    # Foreign Key and Relationships
    company = models.ForeignKey(
        'Company', on_delete=models.PROTECT, related_name='company', help_text=('The company that the control is related'),)
    vendor_control = models.ForeignKey('Control', on_delete=models.PROTECT, null=True, blank=True, related_name='vendor_companycontrol', help_text=(
        'The primary control mapping for the company'),)
    company_control_opex = models.ForeignKey('CompanyControlOpex', on_delete=models.PROTECT, null=True, blank=True, related_name='company_control_opex', help_text=(
        'The control operational expenditures for the company'),)
    company_control_capex = models.ForeignKey('CompanyControlCapex', on_delete=models.PROTECT, null=True, blank=True, related_name='company_control_capex', help_text=(
        'The control captial expenditures for the company'),)
    inline_after = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True, blank=True, related_name='control_before', help_text=(
        'The upstream control id'),)  # If available, this is the control that is upstream.  This will be used for viewing a layer approach to asset secuirity.
    company_locations = models.ManyToManyField('CompanyLocation', blank=True, through='CompanyControlLocation', through_fields=(
        'id_companycontrol', 'id_companylocation'), related_name='CompanyControlLocation', help_text=('Specified geo locations for the company'),)  # Locations of the company control. If 1 then ALL locations.
    company_segments = models.ManyToManyField("CompanySegment", blank=True, through='CompanyControlSegment', through_fields=(
        'id_companycontrol', 'id_companysegment'), related_name='CompanyControlSegment', help_text=('Specified logical segments for the company'),)  # Segments of the company control. If 1 then ALL segments.
    dependencies = models.ManyToManyField("DependencyType", blank=True, through='CompanyControlDependency', through_fields=(
        'id_companycontrol', 'id_controldependency'), related_name='CompanyControlDependents', help_text=('Items the control is dependent on to function effectively.'),)  # Company controls may be dependent on multiple items to function effectively. // Need to figure out how to account for other types of dependencies.  IE Procedural, Distribution, etc....

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Controls")


class CompanyControlMeasure(models.Model):
    """Company Control Measure.  This will be leveraged to determine all the measurements that are reviewed for the controls effectiveness.  Specific control meausres should be tied to the entry based on the threat scenario"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the measure'),)  # Name of the measure for the control used in the entry.
    description = models.TextField(
        blank=False, help_text=('Description of the measurment'),)  # Description of the measure used for the control based on the entry.
    formula = models.CharField(
        max_length=512, blank=True, help_text=('Formula that is used to measure the success of the control'),)  # What is the formula to define the measure.  Need to have a formula builder create for the user to create a measurement.
    unit = models.CharField(
        max_length=128, blank=False, help_text=('Name of the unit of measure'),)  # Name of the unit of measure.  IE  Logs per minute, Updates per Quarter
    baseline = models.CharField(
        max_length=128, blank=True, help_text=('The baseline of the measurement'),)  # The baseline for the control
    target = models.CharField(
        max_length=128, blank=True, help_text=('The target measurement to achieve'),)  # The target outcome to be reached
    tolerance = models.CharField(
        max_length=128, blank=True, help_text=('The tolerance level from target to be considered effective'),)  # Used to determine if the result is within an acceptable range.
    range_toggle = models.BooleanField(default=False, help_text=(
        'Designates whether the measurement is a range or single measure'),)  # If set to False ranges are not used for the measurement.  If True, then ranges for baseline, target, and tolerance will need to be set.  _range values will be the value side of the range inputs.
    baseline_range = models.CharField(
        max_length=128, blank=True, help_text=('The baseline of the measurement'),)  # The baseline for the control
    target_range = models.CharField(
        max_length=128, blank=True, help_text=('The target measurement to achieve'),)  # The target outcome to be reached
    tolerance_range = models.CharField(
        max_length=128, blank=True, help_text=('The tolerance level from target to be considered effective'),)  # Used to determine if the result is within an acceptable range.
    # Foreign Key and Relationships
    company_control = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True, related_name='controlmeasure', help_text=(
        'The measure the associated with the company control'),)

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Measures")


class CompanyControlMeasurementResult(models.Model):
    """Company Control Measure.  Used to trend results for a company control measurement.  May be used to trigger alerts if results are not within the tolerance level"""

    result = models.CharField(
        max_length=128, blank=True, help_text=('The current result of the measurement'),)  # Not in use
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Date the measurement was taken'),)  # Not in use
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='MeasurementUser', help_text=(
        'User id of the user that input the result'),)
    # Foreign Key and Relationships
    measurement = models.ForeignKey('CompanyControlMeasure', on_delete=models.PROTECT, null=True, related_name='companycontrolmeasure', help_text=(
        'The measure the associated with the company control'),)

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Measurement Result")


class CompanyControlOpex(models.Model):
    """Company Control Operational Expenditures.  This will be leveraged to determine all the operational cost specific to the company contorl.  This will be use to measure the annual cost of ownership to support the control"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the operational expendure'),)  # Name of the operational expenditure for the company control.
    detail = models.TextField(
        blank=False, help_text=('Description of the operational expendure'),)  # Description of the operational expenditure for the company control.
    date_purchased = models.DateTimeField(
        blank=True, null=True, help_text=('Date the operational expendure was purchased'),)  # Date of purchase for the operational expenditure for the company control
    amount = models.DecimalField(default=0, blank=True, max_digits=30, decimal_places=2, help_text=(
        'Operational cost spent'),)  # The amount of money spent.
    accounting_id = models.CharField(
        max_length=155, blank=True, null=True, help_text=('Id of control from the company accounting system for mapping costs'),)  # Future use to map detail from the companies accounting system
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this company should be treated as active'),)  # Determines if the company is active
    was_deleted = models.BooleanField(default=False, help_text=(
        'Designates whether this company should be treated as active'),)  # Determines if the company is active
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the deactivated the company'),)  # Date that the company was deactivated
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Timestamp the company was created'),)  # Date that the company was created
    date_modified = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Timestamp the company was modified'),)  # Last date the company record was modified
    was_deleted = models.BooleanField(default=False, help_text=(
        'Designates whether this company should be treated as active'),)  # Determines if the company is active
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the company was created'),)  # Date that the company was deleted by the Account Admin.  Note: Company will not be permenantly deleted.  It will not be viewable to the Account users.
    created_by = models.ForeignKey('User', on_delete=models.PROTECT,  null=True, blank=True, related_name='created_controlopex', help_text=(
        'User id if created by another user'),)  # User that created the company
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='modified_controlopex', help_text=(
        'User id if created by another user'),)  # User that last modfied the company record
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='deactivated_controlopex', help_text=(
        'User id if deactivated by another user'),)  # User that deactivated the company
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='deleted_controlopex', help_text=(
        'User id if deleted by another user'),)   # User that deleted the company.  Note: Company will not be permenantly deleted.  It will not be viewable to the Account users.
    utility_field = models.CharField(
        max_length=30, blank=True, help_text=('Backoffice field used for queries and reporting'),)  # This field is not viewable to the Account users and is used for backoffice reporting and testing.
    bkof_notes = models.TextField(
        blank=True, help_text=('Backoffice notes on company'),)  # This field is not viewable to the Account users and is use for backoffice detail only.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Operational Expenditures")


class CompanyControlCapex(models.Model):
    """Company Control Capital Expenditures.  This will be leveraged to determine all the captial cost specific to the company contorl.  This will be use to measure the annual cost of ownership to support the control"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the captial expendure'),)  # Name of the captial expenditure for the company control.
    detail = models.TextField(
        blank=False, help_text=('Description of the captial expendure'),)  # Description of the captial expenditure for the company control.
    date_purchased = models.DateTimeField(
        blank=True, null=True, help_text=('Date the captial expendure was purchased'),)  # Date of purchase for the captial expenditure for the company control
    amount = models.DecimalField(default=0, blank=True, max_digits=30, decimal_places=2, help_text=(
        'Operational cost spent'),)  # The amount of money spent.
    accounting_id = models.CharField(
        max_length=155, blank=True, null=True, help_text=('Id of control from the company accounting system for mapping costs'),)  # Future use to map detail from the companies accounting system
    invest_range = models.IntegerField(
        default=1, blank=False, help_text=('Range in years to determine the annual investment cost of the control'),)  # This may be used if companies want to distribute the capital expenditure over years from the purchase date.
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this company should be treated as active'),)  # Determines if the company is active
    was_deleted = models.BooleanField(default=False, help_text=(
        'Designates whether this company should be treated as active'),)  # Determines if the company is active
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the deactivated the company'),)  # Date that the company was deactivated
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Timestamp the company was created'),)  # Date that the company was created
    date_modified = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Timestamp the company was modified'),)  # Last date the company record was modified
    was_deleted = models.BooleanField(default=False, help_text=(
        'Designates whether this company should be treated as active'),)  # Determines if the company is active
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the company was created'),)  # Date that the company was deleted by the Account Admin.  Note: Company will not be permenantly deleted.  It will not be viewable to the Account users.
    created_by = models.ForeignKey('User', on_delete=models.PROTECT,  null=True, blank=True, related_name='created_controlcapex', help_text=(
        'User id if created by another user'),)  # User that created the company
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='modified_controlcapex', help_text=(
        'User id if created by another user'),)  # User that last modfied the company record
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='deactivated_controlcapex', help_text=(
        'User id if deactivated by another user'),)  # User that deactivated the company
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='deleted_controlcapex', help_text=(
        'User id if deleted by another user'),)   # User that deleted the company.  Note: Company will not be permenantly deleted.  It will not be viewable to the Account users.
    utility_field = models.CharField(
        max_length=30, blank=True, help_text=('Backoffice field used for queries and reporting'),)  # This field is not viewable to the Account users and is used for backoffice reporting and testing.
    bkof_notes = models.TextField(
        blank=True, help_text=('Backoffice notes on company'),)  # This field is not viewable to the Account users and is use for backoffice detail only.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Capital Expenditures")


class CompanyControlDependency(models.Model):
    """Company Control Dependency."""

    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True, related_name='dependency_companycontrol', help_text=(
        'The company control the dependency is associated'),)
    id_controldependency = models.ForeignKey('DependencyType', on_delete=models.PROTECT, null=True, related_name='companycontrol_dependency', help_text=(
        'The company control the dependency is associated'),)
    row = models.IntegerField(blank=False, help_text=(
        'Identify the dependency type variable'),)  # Used in conjuction with the id_dependencytype selection to identify the dependent.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the control dependency is active'),)  # The only active dependencies should be viewed by Account Users.
    has_contingency = models.BooleanField(
        default=False, help_text=('Designates whether there is a contingency plan in place for the dependency'),)  # Used to determine where gaps may be with control dependencies.
    contingency_plan = models.TextField(
        blank=False, help_text=('Defined contingency plan for the dependency'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    notes = models.TextField(
        blank=False, help_text=('Notes regarding the dependency'),)  # Notes to specify dependency details
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.id_dependencytype

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Dependencies")


class CompanyControlCost(models.Model):
    """Control Cost.  This table will help determine the current and continued cost of the control at the company level.  It will be used to tie the company control with the cost of the control via the company_control field"""

    amount_paid = models.DecimalField(default=0, blank=True, max_digits=12, decimal_places=2, help_text=(
        'Amount paid for the control'),)  # This will determine the total cost of the control.  Licensing, hardware, software, maintenance, subscription, etc.
    EXPENDITURE_CHOICES = (
        ('capex', 'CapEx'),
        ('opex', 'OpEx'),
        ('notspecified', 'Not Specified'),
    )
    # Used to determine how the cost is classifed for accounting purposes.
    expenditure = models.CharField(
        max_length=14, choices=EXPENDITURE_CHOICES, default='notspecified')
    notes = models.TextField(
        blank=False, help_text=('Description of the control cost'),)  # Notes associated with the control payment.
    date_paid = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Date the payment was made
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Date the payment was submitted
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the control cost is active.'),)  #
    company_control = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True, related_name='company_control', help_text=(
        'Type of control cost associated with the entry'),)
    cost_type = models.ForeignKey('CompanyControlCostType', on_delete=models.PROTECT, null=True, related_name='control_costtype', help_text=(
        'Type of control cost associated with the entry'),)  # Used to determine the total annual cost of the control.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Costs")


class CompanyControlCostType(models.Model):
    """Control Cost Type."""

    name = models.CharField(
        max_length=128, help_text=('Model of the control cost type'),)  # Not in use
    description = models.TextField(
        blank=False, help_text=('Description of the control cost type'),)  # Not in use
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the control cost type is active for use'),)
    account = models.ForeignKey(
        'Account', related_name='account_controlcosttype', on_delete=models.PROTECT, help_text=('The account that the control cost type is related'),)  # Companies have the ability to add their own control cost types name.  These will be under review for addtion to CORE.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Cost Types")


class CompanyObjective(models.Model):
    """Company Objective.

    This allows the company to track objectives that support a path to continued profitability.  Company objectives are future state outcomes the company would like to achieve.  Threats that affect these objectives are handled with enablers.
    """

    name = models.CharField(
        max_length=100, blank=False, help_text=('Name of the company objective'),)  # Company to determine the name of the objective
    description = models.TextField(
        blank=True, help_text=('Description about the company objective'),)  # Description of the company objective
    monetary_value_start = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, help_text=(
        'The beginning monetary value of the objective'),)  # The monetary value of the objective at its start date
    monetary_value_end = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, help_text=(
        'The ending monetary value of the objective'),)  # The monetary value of the objective at its end date
    monetary_value_current = models.DecimalField(default=0.00, max_digits=30, decimal_places=2, help_text=(
        'The ending monetary value of the objective'),)  # The current monetary value of the objective for status benchmarking
    date_start = models.DateField(
        null=True, blank=True, help_text=('Date the objective will start'),)  # Dates used to determine current state  and benchmark of the objective
    date_end = models.DateField(
        null=True, blank=True, help_text=('Date the objective will end'),)  # Dates used to determine current state and benchmark of the objective
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the objective was created'),)  # Date the objective was added
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company objective is active.'),)  #
    """Application Input"""
    # Foreign Key and Relationships
    objective_owner = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='companycontact_objective', help_text=(
        ' Who owns the requirement and detail of the objective'),)  # Who leads the objective effort.
    company = models.ForeignKey('Company', on_delete=models.PROTECT, blank=False, related_name='companyobjective', help_text=(
        'Company id for the company has defined the objective'),)  # Company that defined the objective
    risk_types = models.ManyToManyField('RiskType', through='CompanyObjectiveRiskType', through_fields=('id_companyobjective', 'id_risktype'), related_name='CompanyObjectiveRiskTypes', help_text=(
        'Specifies business sector the objective is related'),)  # The objectives can be tied to more than on sector.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Objectives")


class CompanyObjectiveRiskType(models.Model):
    """Entry Risk Type."""

    # Foreign Key and Relationships
    id_companyobjective = models.ForeignKey('CompanyObjective', on_delete=models.CASCADE, null=True, related_name='companyobjectverisktype', help_text=(
        'The objective the associated with the risk type'),)
    id_risktype = models.ForeignKey('RiskType', on_delete=models.CASCADE, null=True, related_name='risktypeobjective', help_text=(
        'The business risk type associated with the objective'),)

    def __str__(self):
        """String."""
        return self.id_risktype.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Objective Risk Types")


class CompanyContact(models.Model):
    """Company Contacts.  Contacts are identifed at the Company level.  When listing POC for a company"""

    first_name = models.CharField(
        max_length=128, blank=False, help_text=('First name'),)  # First name of the contact
    last_name = models.CharField(
        max_length=128, blank=False, help_text=('Last name'),)  # Last name of the contact
    title = models.CharField(
        max_length=255, blank=True, help_text=('Title'),)  # Work title of the contact
    main_poc = models.BooleanField(
        default=False, help_text=('Is the contact a main point of contact?'),)  # Primary point of contact.  Not as relevant for employee type contacts.
    decision_maker = models.BooleanField(
        default=False, help_text=('Is the contact a decsion maker?'),)  # The contact is a decision maker for risk related items.
    description = models.CharField(
        max_length=255, blank=True, help_text=('Description'),)  # Description of the contact
    email = models.EmailField(
        max_length=128, blank=False, unique=True, help_text=('Email address'),)  # Email of the user.  May be used to trigger alerts to Contacts
    office_phone = models.CharField(
        max_length=30, blank=True, help_text=('Office phone'),)  # Office phone number
    office_phone_ext = models.CharField(
        max_length=30, blank=True, help_text=('Office extension'),)  # Office extension
    cell_phone = models.CharField(
        max_length=30, blank=True, help_text=('Cell phone'),)  # Cell phone of Individual
    notes = models.TextField(
        blank=True, help_text=('Notes'),)  # Notes related to the contact
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether this contact should be treated as active'),)  # The contact is active in the account.
    defined1_data = models.CharField(max_length=128, null=True, blank=True, help_text=(
        'Custom company field for company contact table -see company table'),)  # Company defined field
    date_defined1 = models.DateTimeField(null=True, blank=True, help_text=(
        'Custom company field for company contact table -see company table'),)  # Company defined field
    defined2_data = models.CharField(max_length=128, null=True, blank=True, help_text=(
        'Custom company field for company contact table -see company table'),)  # Company defined field
    date_defined2 = models.DateTimeField(null=True, blank=True, help_text=(
        'Custom company field for company contact table -see company table'),)  # Company defined field
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the contact was created'),)  # Date that the contact was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text=('Timestamp the contact was created'),)  # Date that the contact was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the contact was deactivated'),)  # Date the contact was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the contact was created'),)  # Date the contact was deleted
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the asset'),)  # If True, evaluation is needed.
    # Foreign Key and Relationships
    reports_to = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, blank=True, related_name='reports_to_companyindividual', help_text=(
        'Contact id of the supervisor to build a organizational hierachy'),)  # Used to define a organizational hierachy
    user_contact = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='user_contact', help_text=(
        'Used when an account user is added to the company as a contact'),)  # Used to tie an account user to the contact table.  If this populated, there is special logic to align the user_id and the company_contact_id.
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='created_companyindividual', help_text=(
        'User id of the user that created the field'),)  # User id that created the contact
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='modified_companyindividual', help_text=(
        'User id that last modified the field'),)  # User id that modified the contact
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='deactivated_companyindividual', help_text=(
        'User id if deactivated by another user'),)  # User id that deactivated the contact
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='deleted_companyindividual', help_text=(
        'User id if deleted by another user'),)  # User id that deleted the contact
    company = models.ForeignKey(
        'Company', on_delete=models.PROTECT, related_name='company_contact', help_text=('The company that the control is related'),)  # Company the contact is associated
    contact_type = models.ForeignKey(
        'ContactType', on_delete=models.PROTECT, related_name='companycontact', help_text=('The type of contact being described'),)  # Contact could be of type vendor, contractor, or employee.
    vendor = models.ForeignKey(
        'Vendor', on_delete=models.PROTECT, related_name='vendorcontact', null=True, blank=True, help_text=('If vendor is chosen for contact type, which vendor'),)  # If contact is of type contractor or vendor the tie them to the a vendor.

    class Meta:
        """Meta class."""

        indexes = [
            models.Index(fields=['email'], name='email_idx'), ]
        verbose_name_plural = ("Company Contacts")

    def __str__(self):
        """String."""
        return self.first_name
'''
    def get_full_name(self):
        """Get full name."""
        return "{} {}" .format(self.first_name, self.last_name)
'''


class ContactType(models.Model):
    """Contact Type."""

    name = models.CharField(
        max_length=30, blank=False, help_text=('Name of the type of contact'),)  # Contacts may have different types based on the account/company they associated.  Users will also leverage ContactType at the AccountMembership table to determine the default type they will be when added to the CompanyContact record.
    description = models.CharField(
        max_length=255, blank=False, help_text=('Description of the type of contact'),)  # Description of the contact type.
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Contact Types")


class CompanyTeam(models.Model):
    """Company Team."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Team Name'),)  # Name of the team that is created for the company. This team will consists of multiple contacts defined in the company.
    description = models.CharField(
        max_length=255, blank=False, help_text=('Team Description'),)  # Description of the team.
    abbrv = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Team Alias'),)  # Abbreviation of the team.  If not null, will be used when reporting details on the team.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether this company team should be treated as active'),)  # The company team is active in the company.
    # Foreign Key and Relationships
    company = models.ForeignKey(
        'Company', on_delete=models.PROTECT, related_name='company_team', help_text=('The company that the team is related'),)  # Company the team is created
    lead = models.ForeignKey(
        'CompanyContact', on_delete=models.PROTECT, null=True, related_name='company_lead', help_text=('The team lead'),)  # Lead that is associated to the company team.
    member = models.ManyToManyField("CompanyContact", through='CompanyTeamMember',
                                    through_fields=('id_companyteam', 'id_companycontact'), related_name='CompanyTeamMemeberships', help_text=('Contacts that belong to the Company Team'),)  # Contacts may belong to multiple Company Teams.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Teams")


class CompanyTeamMember(models.Model):
    """Company Team Members."""

    id_companyteam = models.ForeignKey(
        'CompanyTeam', on_delete=models.PROTECT, related_name='companyteam', help_text=('The company that the team is related'),)  # Company team that the contact is appart.
    id_companycontact = models.ForeignKey(
        'CompanyContact', on_delete=models.PROTECT, related_name='companyteammember', help_text=('The member of the team'),)  # Contact this is a part of the team.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether this comany team member should be treated as active'),)  # The team member is active in the company team.
    date_added = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the member was added'),)  # Date that the member joined the team.
    removed_date = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the individual was removed'),)  # Date the member was removed from the team.
    # Foreign Key and Relationships
    added_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='added_companyteammembers', help_text=(
        'User id of the user that added the member'),)  # User that added the contact as a member of the team.
    removed_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='removed_companyteammembers', help_text=(
        'User id if removed by another user'),)  # User that removed the contact as a member of the team.

    def __str__(self):
        """String."""
        return self.member

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Team Members")


class CompanyLocation(models.Model):
    """Company Location.  In the future this will be tied to a Geo-Service.  Companies will need to specific at least on location before creating entries.  Assets, entries, contacts, etc. will all have a companylocation association.  This helps break down location specific cost models and risk impact measurements."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the comany location'),)  # Name of the company location
    countrycode = models.CharField(
        max_length=3, blank=False, help_text=('Country code for the company location'),)  # Country code used for the location.  Should use 3 character country code.
    state = models.CharField(
        max_length=128, blank=True, null=True, help_text=('State or providence of the company location'),)  # State or providence of the company location
    city = models.CharField(
        max_length=128, blank=False, help_text=('City of providence of the company location'),)  # City of the company location
    hq = models.BooleanField(
        default=False, help_text=('Headquarters of the company location'),)  # Is the company location the companies headquarters?
    geolat = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Latitude coord of the company location'),)  # Latitude of the company location.
    geolon = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Longitude coord of the company location'),)  # Longitude of the company location.
    abbrv = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Company Location Abbrivation -used for reporting'),)  # If specified, will be used for company location reporting.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether this location should be treated as active'),)  # The location is active in the company.
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the asset'),)  # If True, evaluation is needed.
    """Application Input"""
    # Foreign Key and Relationships
    company = models.ForeignKey(
        'Company', on_delete=models.PROTECT, related_name='companylocation', help_text=('The company that the location is related'),)  # Company the company location belongs to.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Locations")


class CompanyControlLocation(models.Model):
    """Company Control Location."""

    # Foreign Key and Relationships
    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, related_name='control_companylocation', help_text=(
        'The company and control'),)  # Id of the company control
    id_companylocation = models.ForeignKey('CompanyLocation', on_delete=models.PROTECT, related_name='location_companycontrol', help_text=(
        'The company location that the control is used'),)  # Id of the company location.  If 1 is used, this means All locations.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company control location is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not have grant on the company.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Locations")


class CompanySegment(models.Model):
    """Company Segment. This will allow companies to segment risk areas.  Assets, entries, contacts, etc. will all have ability to tie to a segment.  This helps break down segment specific cost models and risk impact measurements."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the comany segment'),)  # Name of the company segment
    description = models.CharField(
        max_length=255, blank=False, help_text=('Segment Description'),)  # Description of the segment.
    abbrv = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Company segment abbrivation -used for reporting'),)  # If specified, will be used for company segment reporting.
    is_physical = models.BooleanField(
        default=False, help_text=('Designates whether this segment should be treated as physical'),)  # It is assumed the segementation is logical unless this is set to True.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether this segment should be treated as active'),)  # The segment is active in the company.
    """Application Input"""
    # Foreign Key and Relationships
    company = models.ForeignKey(
        'Company', on_delete=models.PROTECT, related_name='companysegment', help_text=('The company that the segment is related'),)  # Company the company segment belongs to.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Segments")


class CompanyControlSegment(models.Model):
    """Company Control Segment."""

    # Foreign Key and Relationships
    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, related_name='control_companysegment', help_text=(
        'The company and control'),)  # Id of the company control
    id_companysegment = models.ForeignKey('CompanySegment', on_delete=models.PROTECT, related_name='segment_companycontrol', help_text=(
        'The company segment that the control is used'),)  # Id of the company segment.  If 1 is used, this means All locations.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company control segment is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not have grant on the company.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Segments")


class CompanyFinding(models.Model):
    """CompanyFinding.  Should this be moved directly to the control or is it."""

    description = models.TextField(
        blank=False, help_text=('Description of the finding'),)  # Not in use
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the finding was created'),)  # Not in use
    date_modified = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the findingl was modified'),)  # Not in use
    date_start = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the finding started'),)  # Not in use
    date_stop = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the finding stopped'),)  # Not in use
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the finding was deleted'),)  # Not in use
    effective_impact = models.FloatField(
        null=True, blank=True, help_text=('What percentage of impact to the effectiveness'),)
    # Foreign Key and Relationships
    owner = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='entrycontrolfinding', help_text=(
        ' Who owns the task'),)
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='created_finding', help_text=(
        'User id of the user that created the field'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='modified_finding', help_text=(
        'User id that last modified the field'),)
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='deleted_finding', help_text=(
        'User id if deleted by another user'),)
    effected_controls = models.ManyToManyField('CompanyControl', blank=True, through='CompanyControlFinding', through_fields=(
        'id_companyfinding', 'id_companycontrol'), related_name='CompanyControlFindings', help_text=('Control or controls the finding impacted'),)  # Company findings may be applied to multiple findings.

    def __str__(self):
        """String."""
        return self.desc

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Findings")


class CompanyControlFinding(models.Model):
    """Company Control Contact."""

    # Foreign Key and Relationships
    id_companyfinding = models.ForeignKey('CompanyFinding', on_delete=models.PROTECT, related_name='control_companyfinding', help_text=(
        'The company finding'),)  # Id of the company finding
    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, related_name='finding_companycontrol', help_text=(
        'The company control that had the finding'),)  # Id of the company control.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company control finding is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the finding will not be applied to the control.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Findings")


class CompanyPlaybook(models.Model):
    """This table describes the incident response procedures for the company based on certain use cases.  Playbooks belonging to core company will be leveraged as examples for templates or best practice"""

    name = models.CharField(
        max_length=30, blank=False, help_text=('Name of the incident response playbook'),)  # Name of the IR Playbook
    summary = models.TextField(
        blank=False, help_text=('Executive summary of the incident response playbook'),)  # Description of the playbook
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='created_playbook', help_text=(
        'User id of the user that created the playbook'),)  # User that created the playbook
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='modified_playbook', help_text=(
        'User id that last modified the playbook'),)  # User that last modified the playbook
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='deactivated_playbook', help_text=(
        'User id if deactivated by another user'),)  # User that deactivated the playbook
    playbook_owner = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='owner_playbook', help_text=(
        ' Who owns management of the incident repsonse playbook.  This should be a contributor of the system'),)  # User that currently owns and is held accountable for the incidnet response playbook
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the playbook'),)  # If True, evaluation is needed.  Often used to overide a timed evaluation.
    # Foreign Key and Relationships
    company = models.ForeignKey('Company', on_delete=models.PROTECT, null=True, blank=True, related_name='company_playbook', help_text=(
        'The company that the playbook belongs'),)  # When a company creates a playbook within the application.
    playbook_company_member = models.ManyToManyField('User', through='CompanyPlaybookMember',
                                                     through_fields=('id_company_playbook', 'id_company_member'), related_name='CompanyPlaybookMembers', help_text=('Specifies which company members have a role in the playbook'),)  # Specifies what users have acess to the company.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Playbooks")


class CompanyPlaybookMember(models.Model):
    """User Responsibilities for the playbooks."""

    id_company_playbook = models.ForeignKey('CompanyPlaybook', on_delete=models.CASCADE, null=True, related_name='company_playbook_user', help_text=(
        'The company incident repsonse playbook used if the risk occurs'),)
    id_company_member = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='user_company_playbook', help_text=(
        'The user associated to the company incident response playbook'),)
    member_role = models.ForeignKey('PlaybookRole', on_delete=models.PROTECT, null=True, blank=True, related_name='member_playbook_role', help_text=(
        'The role a member will have for the playbook'),)  # When a member is added to the play book, they will have a role.
    member_responsibilites = models.ManyToManyField('PlaybookResponsibility', through='CompanyPlaybookMemberResponsibility',
                                                    through_fields=('id_company_playbook_member', 'id_playbook_responsibility'), related_name='CompanyPlaybookMemberResponsibilities', help_text=('Specifies which members have responsibilites in the playbook'),)  # Specifies what users have acess to the company.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Playbook Members")


class CompanyPlaybookMemberResponsibility(models.Model):
    """User Responsibilities for the playbooks."""

    id_playbook_responsibility = models.ForeignKey('PlaybookResponsibility', on_delete=models.CASCADE, null=True, related_name='company_playbook_responsibility', help_text=(
        'The responsibility the member has in the playbook if the risk occurs'),)
    id_company_playbook_member = models.ForeignKey('CompanyPlaybookMember', on_delete=models.CASCADE, null=True, related_name='member_company_playbook_responsibility', help_text=(
        'The responsibility associated to the company member for the incident response playbook'),)
    attest_days = models.IntegerField(default=365,
                                      help_text=('Defines the default number of days for the assetation period'),)  # How often a user should attest to their responsibilites
    attest_flg = models.BooleanField(
        default=False, help_text=('Defines if an attestment is due for the playbook responsbility'),)  # If True, attestment is needed.  Often used to overide a timed attestation period.
    date_last_attested = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the company member last attested to the responsibility'),)  # Users must attest to the responsbilities they have for incident response.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Playbook Member Responsibilities")


class CompanyPlaybookAction(models.Model):
    """Actions for the playbook.  What to do in the event the risk entry is realized"""

    action = models.TextField(
        blank=False, help_text=('Description of the action a user must take for the playbook'),)  # The action the user will have for the playbook.
    sequence_order = models.IntegerField(
        blank=True, null=True, help_text=('Sequence the actions should be taken in the playbook.'),)  # Not in use
    attest_days = models.IntegerField(default=365,
                                      help_text=('Defines the default number of days for the assetation period'),)  # How often a user should attest to their actions
    attest_flg = models.BooleanField(
        default=False, help_text=('Defines if an attestment is due for the playbook action'),)  # If True, attestment is needed.  Often used to overide a timed attestation period.
    date_last_attested = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the company member last attested to the responsibility'),)  # Users must attest to the actionss they have for incident response.
    action_type = models.ForeignKey('PlaybookActionType', on_delete=models.CASCADE, null=True, blank=True, related_name='company_playbook_action', help_text=(
        'The type of playbook action'),)  # Actions will be grouped by type and then listed in sequence order
    company_playbook = models.ForeignKey('CompanyPlaybook', on_delete=models.CASCADE, null=True, blank=True, related_name='company_playbook_action', help_text=(
        'The actions assigned in the company playbook'),)
    playbook_action_owner = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='action_owner_playbook', help_text=(
        ' Who owns the action for incident repsonse playbook.'),)  # User that currently owns and is held accountable for the incidnet response playbook action defined.

    def __str__(self):
        """String."""
        return self.action

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Playbook Actions")

'''
class CompanyControlContact(models.Model):
    """Company Control Contact."""

    # Foreign Key and Relationships
    id_companycontrol = models.ForeignKey('CompanyControl', related_name='control_companycontact', help_text=(
        'The company and control'),)  # Id of the company control
    id_companycontact = models.ForeignKey('CompanyContact', related_name='contact_companycontrol', help_text=(
        'The company contact that the control is dependent on'),)  # Id of the company contact.  If 1 is used, this means All locations.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company control contact is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not be a dependent for the control effectiveness.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Dependent Contacts")


class CompanyControlTeam(models.Model):
    """Company Control Team."""

    # Foreign Key and Relationships
    id_companycontrol = models.ForeignKey('CompanyControl', related_name='control_companyteam', help_text=(
        'The company and control'),)  # Id of the company control
    id_companyteam = models.ForeignKey('CompanyTeam', related_name='contact_companycontrol', help_text=(
        'The company team that the control is dependent on'),)  # Id of the company team.  If 1 is used, this means All locations.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company control team is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the team will not be a dependent for the control effectiveness.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Dependent Teams")


class CompanyControlVendor(models.Model):
    """Company Control Vendor."""

    # Foreign Key and Relationships
    id_companycontrol = models.ForeignKey('CompanyControl', related_name='control_companyvendor', help_text=(
        'The company and control'),)  # Id of the company control
    id_companyvendor = models.ForeignKey('Vendor', related_name='vendor_companycontrol', help_text=(
        'The vendor that the control is dependent on'),)  # Id of the company vendor.  If 1 is used, this means All locations.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the company control vendor is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the vendor will be a dependent for the control effectiveness.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Dependent Vendors")
'''
