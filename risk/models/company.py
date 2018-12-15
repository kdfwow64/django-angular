"""Company & related models."""
from django.db import models
from risk.models.auth import User, UserGrant
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
)


class Company(DefaultFields):
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
    # If False, use Fixed Loss for calculations.  If True, use PAR loss for
    # calculations.
    monetary_value_toggle = models.CharField(choices=Selector.LOSS, default='F', max_length=1, help_text=(
        'Toggle to determine if company max loss is measured by fixed=False or par =True monetary value'),)
    annual_revenue = models.DecimalField(blank=True, default=0, max_digits=30, decimal_places=2, help_text=(
        'Annual revenue of the company. Requred if the toggle is set to par_max_loss'),)  # Annual revenue of the company.  Carried to 2 decimal places in case this is written via API from other system.
    weight_frequency = models.FloatField(default=1, help_text=(
        'Company specific weighted value for frequency'),)  # In special cases based on the type of business.  The frequency weight may need to be adjusted.
    weight_impact = models.FloatField(default=1, help_text=(
        'Company specific weighted value for impact'),)  # In special cases based on the type of business the impact weight may need to be adjusted.  Defaults to a 1 multiplier
    weight_severity = models.FloatField(default=1, help_text=(
        'Company specific weighted value for severity'),)  # In special cases based on the type of business the severity weight may need to be adjusted.  Defaults to a 1 multiplier
    resilience_max = models.IntegerField(blank=True, null=True, help_text=(
        'Maximum number of units any control has to recover'),)  # Resilience time is used to determine if there are controls that may not recover in an appropirate time frame.
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
    utility_field = models.CharField(
        max_length=30, blank=True, help_text=('Backoffice field used for queries and reporting'),)  # This field is not viewable to the Account users and is used for backoffice reporting and testing.
    bkof_notes = models.TextField(
        blank=True, help_text=('Backoffice notes on company'),)  # This field is not viewable to the Account users and is use for backoffice detail only.
    account = models.ForeignKey('Account', on_delete=models.PROTECT, blank=False, related_name='account_company', help_text=(
        'The account the company was created under'),)  # The account the company was created from.
    naics = models.ForeignKey('Naics', on_delete=models.PROTECT, null=True, blank=True, related_name='naics_company', help_text=(
        'The NAICS code the defines the clients vertical / industry'),)  # The NAICS code for the company.  This is important for vertical reporting.  Account Admin should be able leverage a search function to determine the companies NAICS from the company profile page.
    resilience_unit = models.ForeignKey(
        'TimeUnit', on_delete=models.PROTECT, default=3, null=True, related_name='maxresilienceunit', help_text=('Resilience time unit of the company control'),)  # This setting combined with resilience_max will define the maximum time it should take to recover any control.
    currency_type = models.ForeignKey('CurrencyType', on_delete=models.PROTECT, default=1, blank=False, related_name='currencytype_company', help_text=(
        'Type of currency the company uses for financing'),)  # This will be used to determine the type of currency a company will leverage for the tool.  It should be determined before the cost loss is generated.  Monetary value logic will need to created based off this setting.  USD by default.
    user_member = models.ManyToManyField('User', through='CompanyMember',
                                         through_fields=('id_company', 'id_user'), related_name='CompanyUserMembers', help_text=('Specifies what users have access to the company'),)  # Specifies what users have acess to the company.

    class Meta:
        """Meta class."""
        ordering = ['account']
        verbose_name_plural = ("Companies")

    def __str__(self):
        """String."""
        return self.name

    def get_active_register(self):
        """Get active register for this company."""
        # Return first for timebeing.
        return self.company_register.first()

    def get_company_max_loss(self):
        """Get the company's max loss value."""
        if self.exposure_factor_toggle == 'P':
            # The contributor has chosen a percentage of the annual revenue
            return (self.annual_revenue * self.par_max_loss)
        elif self.monetary_value_togglee == 'F':
                # The contributor has chosen the a fixed monetary amount
            return (self.fixed_max_loss)


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


class CompanyMember(DefaultFields):
    ''' This table is used to tie users to a specific company.  '''
    id_user = models.ForeignKey(
        'User', on_delete=models.PROTECT)  # User Id from the User table
    # Company Id from the Company table
    id_company = models.ForeignKey('Company', on_delete=models.PROTECT)
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


class CompanyMemberGrant(DefaultFields):
    """Company Member Grant."""

    # Foreign Key and Relationships
    id_companymember = models.ForeignKey('CompanyMember', on_delete=models.PROTECT, related_name='grant_companymember', help_text=(
        'The company member that gets a grant'),)  # Id of the company member
    id_usergrant = models.ForeignKey('UserGrant', on_delete=models.PROTECT, related_name='member_usergrant', help_text=(
        'The grant assigned to the company member'),)  # Id of the grant assigned to the company member.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Member Grants")

    def __str__(self):
        """String."""
        # return self.id_companymember
        return self.id_companymember


class CompanyMemberRole(DefaultFieldsCompany):
    """ The role the member plays in the company."""

    company_member_role_type = models.ForeignKey(
        'CompanyMemberRoleType', blank=True, null=True, related_name='company_memberroletype', on_delete=models.PROTECT, help_text=('The role type that the member role is related'),)  # The type of role the member belongs to.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Member Roles")


class CompanyMemberRoleType(DefaultFieldsCompany):
    """ The type of role of the company member"""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Member Role Types")


class CompanyAsset(DefaultFieldsCompany):
    """Company Asset.

    This allows the company to add multiple asset types to their register
    entries.  Companies will define the asset then determine what type of asset it is, along with the ability to group assets for reporting
    """
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
    asset_value_toggle = models.CharField(choices=Selector.ASSET, default='F', max_length=1,
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
        if asset_value_toggle == 'F':
            # Fixed - The asset value has a fixed cost.  Total value may
            # flucuate based on quantity
            return (self.asset_value_fixed * self.asset_quantity_fixed)
        elif asset_value_toggle == 'P':
            # PAR -  The asset value is based on a percentage of revenue for
            # the company
            return (self.asset_value_par * self.id_company.annual_revenue)
        elif asset_value_toggle == 'T':
            # Time based  - The asset has a time based value.  The contributor
            # must determine what is relative.
            return (self.asset_value_timed * self.asset_timed_quantity_relative)


class CompanyAssetType(DefaultFieldsCategory):
    """
    Asset Type.

    Assets may come in many types both tangable (physical device)and
    intangable (business process).  This table describes the asset type.
    """

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Asset Types")


class CompanyAssetSegment(DefaultFields):
    """Company Asset Segment."""

    # Foreign Key and Relationships
    id_companyasset = models.ForeignKey('CompanyAsset', on_delete=models.PROTECT, related_name='asset_companysegment', help_text=(
        'The company and asset'),)  # Id of the company control
    id_companysegment = models.ForeignKey('CompanySegment', on_delete=models.PROTECT, related_name='segment_companyasset', help_text=(
        'The company segment that the asset is used'),)  # Id of the company segment.  If 1 is used, this means All locations.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Asset Segments")


class CompanyAssetLocation(DefaultFields):
    """Company Asset Location."""

    # Foreign Key and Relationships
    id_companyasset = models.ForeignKey('CompanyAsset', on_delete=models.PROTECT, related_name='asset_companylocation', help_text=(
        'The company and control'),)  # Id of the company control
    id_companylocation = models.ForeignKey('CompanyLocation', on_delete=models.PROTECT, related_name='location_companyasset', help_text=(
        'The company location that the asset is located'),)  # Id of the company location.  If 1 is used, this means All locations.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Asset Locations")


class CompanyControl(DefaultFieldsCompany):
    """Company Control.  This table will tie companies to the available controls in the Control table"""

    abbrv = models.CharField(
        max_length=30, blank=True, help_text=('Abbreviation'),)  # Abbreviation of the company control.  Will be used in reporting if present.
    alias = models.CharField(
        max_length=128, blank=True, help_text=('Alias'),)  # Alias used for the company control.  Will be used for reporting if present.
    version = models.CharField(
        max_length=100, blank=True, help_text=('Current version'),)  # Version used for the company control.  Could be policy version, release version,etc It depends on the control defined.
    estimated_opex = models.DecimalField(default=0, blank=True, max_digits=30, decimal_places=2, help_text=(
        'Annual cost for the control. subscription, licensing, etc. (-dependencies)'),)  # Normally 18% of capital expendure if applicable.  Control costs are captured in the CompanyControlCost table, this field is used for future projections.  Capex is handled via the CompanyControlCapex model.
    date_maint = models.DateField(null=True, blank=True, help_text=(
        'Annual maintenance date'),)  # Used to determine annual date that maintenance is completed for the control.
    centeralized = models.BooleanField(default=True, help_text=(
        'Centralized or decentralized'),)  # If True, the control is a centralized control.  If False, the control is decentralized.
    budgeted = models.BooleanField(default=True, help_text=(
        'Annually budgeted'),)  # Not in use
    recovery_multiplier = models.FloatField(blank=True, null=True, help_text=(
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
    control = models.ForeignKey('Control', on_delete=models.PROTECT, null=True, blank=True, related_name='control_companycontrol', help_text=(
        'The control that is mapped to the company'),)
    inline_after = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True, blank=True, related_name='control_before', help_text=(
        'The upstream control id'),)  # If available, this is the control that is upstream.  This will be used for viewing a layer approach to asset secuirity.
    company_locations = models.ManyToManyField('CompanyLocation', blank=True, through='CompanyControlLocation', through_fields=(
        'id_companycontrol', 'id_companylocation'), related_name='CompanyControlLocation', help_text=('Specified geo locations for the company'),)  # Locations of the company control. If 1 then ALL locations.
    company_segments = models.ManyToManyField('CompanySegment', blank=True, through='CompanyControlSegment', through_fields=(
        'id_companycontrol', 'id_companysegment'), related_name='CompanyControlSegment', help_text=('Specified logical segments for the company'),)  # Segments of the company control. If 1 then ALL segments.
    cost_contact = models.ManyToManyField('CompanyContact', blank=True, through='CompanyControlContactCost', through_fields=(
        'id_companycontrol', 'id_companycontact'), related_name='CompanyControl_ContactCost', help_text=('Staff or consultants cost required for the control to function effectively'),)  # Staff or consultants may be required to configure or maintain the control
    cost_vendor = models.ManyToManyField('Vendor', blank=True, through='CompanyControlVendorCost', through_fields=(
        'id_companycontrol', 'id_vendor'), related_name='CompanyControl_VendorCost', help_text=('Vendor cost required for the control to function effectively'),)  # This should default to the vendor for the control, however there may be a dependancy from other vendors for the control to function correctly.  IE.  Electric, Data Center, Control Vendor, etc.
    process_contact = models.ManyToManyField('CompanyContact', blank=True, through='CompanyControlContactProcess', through_fields=(
        'id_companycontrol', 'id_companycontact'), related_name='CompanyControl_ContactProcess', help_text=('Staff or consultant processes that are required for the control to function effectively'),)  # Staff or consultants may be required to configure or maintain the control
    process_vendor = models.ManyToManyField('Vendor', blank=True, through='CompanyControlVendorProcess', through_fields=(
        'id_companycontrol', 'id_vendor'), related_name='CompanyControl_VendorProcess', help_text=('Vendor processes that are required for the control to function effectively'),)  # This should default to the vendor for the control, however there may be a dependancy from other vendors for the control to function correctly.  IE.  Electric, Data Center, Control Vendor, etc.
    process_team = models.ManyToManyField('CompanyTeam', blank=True, through='CompanyControlTeamProcess', through_fields=(
        'id_companycontrol', 'id_companyteam'), related_name='CompanyControl_TeamProcess', help_text=('Team processes that are required for the control to function effectively'),)  # Company controls may be dependent on other teams to function effectively.  For example, this could be a workflow process or a required task...

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Controls")


class CompanyControlMeasure(DefaultFieldsCompany):
    """Company Control Measure.  This will be leveraged to determine all the measurements that are reviewed for the controls effectiveness.  Specific control meausres should be tied to the entry based on the threat scenario"""

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


class CompanyControlMeasurementResult(DefaultFields):
    """Company Control Measure.  Used to trend results for a company control measurement.  May be used to trigger alerts if results are not within the tolerance level"""

    result = models.CharField(
        max_length=128, blank=True, help_text=('The current result of the measurement'),)  # Not in use
    # Foreign Key and Relationships
    measurement = models.ForeignKey('CompanyControlMeasure', on_delete=models.PROTECT, null=True, related_name='companycontrolmeasure', help_text=(
        'The measure the associated with the company control'),)

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Measurement Result")


class CompanyControlCapex(DefaultFields):
    """Company Control Capital Expenditures.  This will be leveraged to determine all the captial cost specific to the company control.  This will be use to measure the annual cost of ownership to support the control"""

    description = models.TextField(blank=True, null=True, help_text=(
        'Description of the field'),)  # Description of the field.
    date_purchased = models.DateField(
        blank=True, null=True, help_text=('Date the captial expendure was purchased'),)  # Date of purchase for the captial expenditure for the company control
    amount = models.DecimalField(default=0, blank=True, max_digits=30, decimal_places=2, help_text=(
        'Operational cost spent'),)  # The amount of money spent.
    accounting_id = models.CharField(
        max_length=155, blank=True, null=True, help_text=('Id of control from the company accounting system for mapping costs'),)  # Future use to map detail from the companies accounting system
    invest_range = models.IntegerField(
        default=1, blank=False, help_text=('Range in years to determine the annual investment cost of the control'),)  # This may be used if companies want to distribute the capital expenditure over years from the purchase date.
    utility_field = models.CharField(
        max_length=30, blank=True, help_text=('Backoffice field used for queries and reporting'),)  # This field is not viewable to the Account users and is used for backoffice reporting and testing.
    bkof_notes = models.TextField(
        blank=True, help_text=('Backoffice notes on company'),)  # This field is not viewable to the Account users and is use for backoffice detail only.
    company_control = models.ForeignKey('CompanyControl', default=1, on_delete=models.PROTECT, blank=False, related_name='%(app_label)s_%(class)s_related_companycontrol', help_text=(
        'Company control id for the capital expenditure related to the control'),)  # Company that defined the field.
    company = models.ForeignKey('Company', default=1, on_delete=models.PROTECT, blank=False, related_name='%(app_label)s_%(class)s_related_company', help_text=(
        'Company id for the company that manages the field'),)  # Company that defined the field.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Capital Expenditures")
        indexes = [
            models.Index(fields=['company']),
        ]

    def __str__(self):
        """String."""
        return self.description

    def get_annual_capex(self):
        """Get active register for this company."""
        # Return first for timebeing.
        return (self.amount / self.invest_range)


class CompanyControlContactCost(DefaultFields):
    """Company Control Dependency."""

    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True, related_name='companycontactcost_companycontrol', help_text=(
        'The company contact the company control is dependent to function effectively'),)
    id_companycontact = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='companycontrol_companycontactcost', help_text=(
        'The company contact that the control depends on to work effectively'),)
    time_allocation = models.FloatField(
        blank=True, null=True, help_text=('Annual percentage of time dedicated by the contact'),)  # This is the time that a contact is dedicated to the control.  It will be used to allot a percentage of the CompanyContact.get_contact_cost.  Logic needs to be built that prevents a contact from allocating more than 100% of their time between multiple controls.
    has_contingency = models.BooleanField(
        default=False, help_text=('Designates whether there is a contingency plan in place for the dependency'),)  # Used to determine where gaps may be with control dependencies.
    contingency_plan = models.TextField(
        blank=True, null=True, help_text=('Defined contingency plan for the dependency'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    notes = models.TextField(
        blank=True, null=True, help_text=('Notes regarding the dependency costs'),)  # Notes to specify dependency details
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Contact Costs")


class CompanyControlVendorCost(DefaultFields):
    """Company Control Dependency."""

    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True, related_name='vendorcost_companycontrol', help_text=(
        'The company control the dependency is associated'),)
    id_vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=True, related_name='companycontrol_vendorcost', help_text=(
        'The vendor the company control is dependent on to function effectively'),)
    allocated_cost = models.DecimalField(default=0, blank=True, max_digits=30, decimal_places=2, help_text=(
        'Annual allocated vendor cost to support the control.'),)  # This could be an annualized cost to support the control.
    has_contingency = models.BooleanField(
        default=False, help_text=('Designates whether there is a contingency plan in place for the dependency'),)  # Used to determine where gaps may be with control dependencies.
    contingency_plan = models.TextField(
        blank=True, null=True, help_text=('Defined contingency plan for the dependency'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    notes = models.TextField(
        blank=True, null=True, help_text=('Notes regarding the dependency costs'),)  # Notes to specify dependency details
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Vendor Costs")


class CompanyControlContactProcess(DefaultFields):
    """Company Control Dependency."""

    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True,
                                          related_name='contactprocess_companycontrol', help_text=('The company control the dependency is associated'),)
    id_companycontact = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='companycontrol_contactprocess', help_text=(
        'The company contact that completes the process for the control to work effectively'),)
    process = models.TextField(
        blank=True, null=True, help_text=('Summary of the process that should occur for the control to work effectively'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    has_contingency = models.BooleanField(
        default=False, help_text=('Designates whether there is a contingency plan in place for the dependency'),)  # Used to determine where gaps may be with control dependencies.
    contingency_plan = models.TextField(
        blank=True, null=True, help_text=('Defined contingency plan for the dependency'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    notes = models.TextField(
        blank=True, null=True, help_text=('Notes regarding the dependency'),)  # Notes to specify dependency details
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Contact Processes")


class CompanyControlVendorProcess(DefaultFields):
    """Company Control Dependency."""

    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True,
                                          related_name='vendorprocess_companycontrol', help_text=('The company control the dependency is associated'),)
    id_vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=True, related_name='companycontrol_vendorprocess', help_text=(
        'The vendor the company control is dependent on to function effectively'),)
    process = models.TextField(
        blank=True, null=True, help_text=('Summary of the process that should occur for the control to work effectively'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    has_contingency = models.BooleanField(
        default=False, help_text=('Designates whether there is a contingency plan in place for the dependency'),)  # Used to determine where gaps may be with control dependencies.
    contingency_plan = models.TextField(
        blank=True, null=True, help_text=('Defined contingency plan for the dependency'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    notes = models.TextField(
        blank=True, null=True, help_text=('Notes regarding the dependency'),)  # Notes to specify dependency details
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Vendor Processes")


class CompanyControlTeamProcess(DefaultFields):
    """Company Control Dependency."""

    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, null=True,
                                          related_name='teamprocess_companycontrol', help_text=('The company control the dependency is associated'),)
    id_companyteam = models.ForeignKey('CompanyTeam', on_delete=models.PROTECT, null=True, related_name='companycontrol_teamprocess', help_text=(
        'The company control the dependency is associated'),)
    process = models.TextField(
        blank=True, null=True, help_text=('Summary of the process that should occur for the control to work effectively'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    has_contingency = models.BooleanField(
        default=False, help_text=('Designates whether there is a contingency plan in place for the dependency'),)  # Used to determine where gaps may be with control dependencies.
    contingency_plan = models.TextField(
        blank=True, null=True, help_text=('Defined contingency plan for the dependency'),)  # This may be moved to its own contingency table.  Can only be populated if has_contingency is set to True.
    notes = models.TextField(
        blank=True, null=True, help_text=('Notes regarding the dependency'),)  # Notes to specify dependency details
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Team Processes")


class CompanyControlCost(DefaultFields):
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


class CompanyControlCostType(DefaultFieldsCompany):
    """Control Cost Type."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Cost Types")


class CompanyObjective(DefaultFieldsCompany):
    """Company Objective.

    This allows the company to track objectives that support a path to continued profitability.  Company objectives are future state outcomes the company would like to achieve.  Threats that affect these objectives are handled with enablers.
    """

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
    """Application Input"""
    # Foreign Key and Relationships
    objective_owner = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='companycontact_objective', help_text=(
        ' Who owns the requirement and detail of the objective'),)  # Who leads the objective effort.
    risk_types = models.ManyToManyField('RiskType', through='CompanyObjectiveRiskType', through_fields=('id_companyobjective', 'id_risktype'), related_name='CompanyObjectiveRiskTypes', help_text=(
        'Specifies business sector the objective is related'),)  # The objectives can be tied to more than on sector.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Objectives")


class CompanyObjectiveRiskType(DefaultFields):
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


class CompanyContact(DefaultFields):
    """Company Contacts.  Contacts are identifed at the Company level.  When listing POC for a company"""

    first_name = models.CharField(
        max_length=60, blank=False, help_text=('First name'),)  # First name of the contact
    last_name = models.CharField(
        max_length=60, blank=False, help_text=('Last name'),)  # Last name of the contact
    main_poc = models.BooleanField(
        default=False, help_text=('Is the contact a main point of contact?'),)  # Primary point of contact.  Not as relevant for employee type contacts.
    decision_maker = models.BooleanField(
        default=False, help_text=('Is the contact a decsion maker?'),)  # The contact is a decision maker for risk related items.
    description = models.CharField(
        max_length=255, blank=True, null=True, help_text=('Description'),)  # Description of the contact
    email = models.EmailField(
        max_length=128, blank=False, help_text=('Email address'),)  # Email of the user.  May be used to trigger alerts to Contacts
    office_phone = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Office phone'),)  # Office phone number
    office_phone_ext = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Office extension'),)  # Office extension
    cell_phone = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Cell phone'),)  # Cell phone of Individual
    notes = models.TextField(
        blank=True, null=True, help_text=('Notes'),)  # Notes related to the contact
    defined1_data = models.CharField(max_length=128, null=True, blank=True, help_text=(
        'Custom company field for company contact table -see company table'),)  # Company defined field
    date_defined1 = models.DateTimeField(null=True, blank=True, help_text=(
        'Custom company field for company contact table -see company table'),)  # Company defined field
    defined2_data = models.CharField(max_length=128, null=True, blank=True, help_text=(
        'Custom company field for company contact table -see company table'),)  # Company defined field
    date_defined2 = models.DateTimeField(null=True, blank=True, help_text=(
        'Custom company field for company contact table -see company table'),)  # Company defined field
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the asset'),)  # If True, evaluation is needed.
    cost_base_salary = models.DecimalField(default=0, max_digits=30, decimal_places=2, help_text=(
        'Annual base salary of the contact'),)  # This will be used to determine dependancy control costs.  Avg. 70k
    # FICA 6.2%, Medicare 1.45%, Workmans Comp .03%-7.5%, etc  Should be
    # multiplied by cost_base_salary. Avg. 8%
    cost_employee_tax = models.FloatField(
        blank=True, null=True, help_text=('Corporate annual tax costs if employee'),)
    cost_employee_benefits = models.DecimalField(default=0, max_digits=30, decimal_places=2, help_text=(
        'Annual cost for benefits'),)  # Cost for company benefits.  IE Insurance, 401k, Dental, Vision  Avg. $5000
    cost_equipment = models.DecimalField(default=0, max_digits=30, decimal_places=2, help_text=(
        'Annual cost for employee equipment'),)  # This value should take a refresh rate into account for tangible assets. IE laptop value / 5yrs.  Avg. $3500
    cost_space = models.DecimalField(default=0, max_digits=30, decimal_places=2, help_text=(
        'Annual cost for the space to house the employee'),)  # Annual cost of sqft should calculated.  Avg. $2000
    cost_travel = models.DecimalField(default=0, max_digits=30, decimal_places=2, help_text=(
        'Annual cost for travel'),)  # Average cost for travel realted to controls
    cost_training = models.DecimalField(default=0, max_digits=30, decimal_places=2, help_text=(
        'Annual cost for training and education'),)  # Estimated cost for training and education
    # Foreign Key and Relationships
    title = models.ForeignKey('JobTitle', on_delete=models.PROTECT, null=True, blank=True, related_name='jobtitle_companyindividual', help_text=(
        'Job title of the company contact'),)  # Used to categorize job titles
    reports_to = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, blank=True, related_name='reports_to_companyindividual', help_text=(
        'Contact id of the supervisor to build a organizational hierachy'),)  # Used to define a organizational hierachy
    user_contact = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='user_contact', help_text=(
        'Used when an application user is added to the company as a contact'),)  # Used to tie an account user to the contact table.  If this populated, there is special logic to align the user_id and the company_contact_id.
    company = models.ForeignKey(
        'Company', on_delete=models.PROTECT, related_name='companycontact', help_text=('The company that the control is related'),)  # Company the contact is associated
    contact_type = models.ForeignKey(
        'ContactType', on_delete=models.PROTECT, related_name='companycontacttype', help_text=('The type of contact being described'),)  # Contact could be of type vendor, contractor, or employee.
    vendor = models.ForeignKey(
        'Vendor', on_delete=models.PROTECT, related_name='vendorcontact', null=True, blank=True, help_text=('If vendor is chosen for contact type, which vendor'),)  # If contact is of type contractor or vendor the tie them to the a vendor.

    class Meta:
        """Meta class."""

        indexes = [
            models.Index(fields=['email'], name='email_idx'), ]
        unique_together = (('email', 'company'),)
        verbose_name_plural = ("Company Contacts")

    def __str__(self):
        """String."""
        return self.get_full_name()

    def get_contact_cost(self):

        return (self.cost_base_salary + (cost_base_salary * cost_employee_tax) +
                cost_employee_benefits + cost_equipment + cost_space + cost_travel +
                cost_training)

    def get_full_name(self):
        """Get full name."""
        return "{} {}" .format(self.first_name, self.last_name)
    get_full_name.short_description = 'Name'


class ContactType(DefaultFieldsCompany):
    """Contact Type."""

    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Contact Types")

    def __str__(self):
        """String."""
        return self.name


class CompanyTeam(DefaultFieldsCompany):
    """Company Team."""

    abbrv = models.CharField(
        max_length=5, blank=True, null=True, help_text=('Team Alias'),)  # Abbreviation of the team.  If not null, will be used when reporting details on the team.
    lead = models.ForeignKey(
        'CompanyContact', on_delete=models.PROTECT, null=True, related_name='company_lead', help_text=('The team lead'),)  # Lead that is associated to the company team.
    member = models.ManyToManyField("CompanyContact", through='CompanyTeamMember',
                                    through_fields=('id_companyteam', 'id_companycontact'), related_name='CompanyTeamMemeberships', help_text=('Contacts that belong to the Company Team'),)  # Contacts may belong to multiple Company Teams.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Teams")

    def __str__(self):
        """String."""
        return self.name


class CompanyTeamMember(DefaultFields):
    """Company Team Members."""

    id_companyteam = models.ForeignKey(
        'CompanyTeam', on_delete=models.PROTECT, related_name='companyteam', help_text=('The company that the team is related'),)  # Company team that the contact is appart.
    id_companycontact = models.ForeignKey(
        'CompanyContact', on_delete=models.PROTECT, related_name='companyteammember', help_text=('The member of the team'),)  # Contact this is a part of the team.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Team Members")

    def __str__(self):
        """String."""
        return self.member


class CompanyLocation(DefaultFieldsCompany):
    """Company Location.  In the future this will be tied to a Geo-Service.  Companies will need to specific at least on location before creating entries.  Assets, entries, contacts, etc. will all have a companylocation association.  This helps break down location specific cost models and risk impact measurements."""

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
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the asset'),)  # If True, evaluation is needed.
    """Application Input"""
    # Foreign Key and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Locations")

    def __str__(self):
        """String."""
        return self.name


class CompanyControlLocation(DefaultFields):
    """Company Control Location."""

    # Foreign Key and Relationships
    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, related_name='control_companylocation', help_text=(
        'The company and control'),)  # Id of the company control
    id_companylocation = models.ForeignKey('CompanyLocation', on_delete=models.PROTECT, related_name='location_companycontrol', help_text=(
        'The company location that the control is used'),)  # Id of the company location.  If 1 is used, this means All locations.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Locations")


class CompanySegment(DefaultFieldsCompany):
    """Company Segment. This will allow companies to segment risk areas.  Assets, entries, contacts, etc. will all have ability to tie to a segment.  This helps break down segment specific cost models and risk impact measurements."""

    is_physical = models.BooleanField(
        default=False, help_text=('Designates whether this segment should be treated as physical'),)  # It is assumed the segementation is logical unless this is set to True.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Segments")


class CompanyControlSegment(DefaultFields):
    """Company Control Segment."""

    # Foreign Key and Relationships
    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, related_name='control_companysegment', help_text=(
        'The company and control'),)  # Id of the company control
    id_companysegment = models.ForeignKey('CompanySegment', on_delete=models.PROTECT, related_name='segment_companycontrol', help_text=(
        'The company segment that the control is used'),)  # Id of the company segment.  If 1 is used, this means All locations.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Segments")


class CompanyFinding(DefaultFields):
    """CompanyFinding.  Should this be moved directly to the control or is it."""

    description = models.TextField(
        blank=False, help_text=('Description of the finding'),)  # Not in use
    date_start = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the finding started'),)  # Not in use
    date_stop = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the finding stopped'),)  # Not in use
    effective_impact = models.FloatField(
        null=True, blank=True, help_text=('What percentage of impact to the effectiveness'),)
    # Foreign Key and Relationships
    owner = models.ForeignKey('CompanyContact', on_delete=models.PROTECT, null=True, related_name='entrycontrolfinding', help_text=(
        ' Who owns the task'),)
    effected_controls = models.ManyToManyField('CompanyControl', blank=True, through='CompanyControlFinding', through_fields=(
        'id_companyfinding', 'id_companycontrol'), related_name='CompanyControlFindings', help_text=('Control or controls the finding impacted'),)  # Company findings may be applied to multiple findings.

    def __str__(self):
        """String."""
        return self.desc

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Findings")


class CompanyControlFinding(DefaultFields):
    """Company Control Contact."""

    # Foreign Key and Relationships
    id_companyfinding = models.ForeignKey('CompanyFinding', on_delete=models.PROTECT, related_name='control_companyfinding', help_text=(
        'The company finding'),)  # Id of the company finding
    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.PROTECT, related_name='finding_companycontrol', help_text=(
        'The company control that had the finding'),)  # Id of the company control.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Control Findings")


class CompanyPlaybook(DefaultFieldsCompany):
    """This table describes the incident response procedures for the company based on certain use cases.  Playbooks belonging to core company will be leveraged as examples for templates or best practice"""

    playbook_owner = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='owner_playbook', help_text=(
        ' Who owns management of the incident repsonse playbook.  This should be a contributor of the system'),)  # User that currently owns and is held accountable for the incidnet response playbook
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the playbook'),)  # If True, evaluation is needed.  Often used to overide a timed evaluation.
    # Foreign Key and Relationships
    playbook_company_member = models.ManyToManyField('User', through='CompanyPlaybookMember',
                                                     through_fields=('id_company_playbook', 'id_company_member'), related_name='CompanyPlaybookMembers', help_text=('Specifies which company members have a role in the playbook'),)  # Specifies what users have acess to the company.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Company Playbooks")


class CompanyPlaybookMember(DefaultFields):
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


class CompanyPlaybookMemberResponsibility(DefaultFields):
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


class CompanyPlaybookAction(DefaultFields):
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
