"""Register Entries & related models."""
from django.db import models


class Register(models.Model):
    """Register.  Primary register that holds all entries."""

    NAME_CHOICES = (
        ('primary', 'Primary'),
        ('demo', 'Demo'),
        ('backup', 'Backup'),
    )
    # Used to determine how the cost is classifed for accounting purposes.
    name = models.CharField(
        max_length=14, choices=NAME_CHOICES, default='primary', blank=False, help_text=('Name of the company register '),)  # Name of the company register. There should only be 1 register per company, however special circumstances may require addtional registers such as transition, backup, demo, etc.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Date the register was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Date the register was last modified.  This will be set with any entry modifications.
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the individual was deactivated'),)  # Date the regsiter was deactivated.
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Date the register was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='created_register', help_text=(
        'User id of the user that created the field'),)  # User that created the register
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='modified_register', help_text=(
        'User id that last modified the field'),)  # User that last modified the regsiter
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='deactivated_register', help_text=(
        'User id if deactivated by another user'),)  # Users that deactivated the register
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='deleted_register', help_text=(
        'User id if deleted by another user'),)  # User that deleted the register
    company = models.ForeignKey('Company', on_delete=models.PROTECT, blank=False, related_name='company_register', help_text=(
        'Company id for the register.'),)  # Company that the register is associated.

    def __str__(self):
        """String."""
        return self.name


class Entry(models.Model):
    """Entry."""

    summary = models.CharField(
        max_length=128, blank=False, help_text=('Brief description of the risk'),)  # Brief summary of the risk to be tracked.  Specifically used when listing entries.
    desc = models.TextField(
        blank=False, help_text=('Description broader description of the registery entry'),)  # More content to provide a better understanding of the risk.
    entry_number = models.IntegerField(
        blank=True, null=True, help_text=('The number that is displayed to the client for the register'),)  # This is the number viewable to the user.  The companies should not see the actual entry id in the application.  Logic will need to be used to find the last entry id for a company and add.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the entry is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the entry has been revoked on the company.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the individual was created'),)  # User that created the risk entry
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text=('Timestamp the individual was created'),)  # Date the risk entry was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the individual was deactivated'),)  # Date the risk was deactivated.  Should be set when the entry is revoked.
    frequency_multiplier = models.FloatField(
        default=1, blank=True, null=True, help_text=('Used to multiple the number of occurrences on an annual basis to determine total frequency per year.'),)  # This used to determine the number of times annual the risk may occur.  Logic in the application will be used to set the number. IE 6 times a year = 6, every 2 years = .5
    frequency_notes = models.TextField(
        blank=True, help_text=('Additional notes from the contributor regarding the frequency calculation.'),)  # Notes regarding the frequency of the threat event
    impact_notes = models.TextField(
        blank=True, help_text=('Notes regarding the impact logic'),)  # Notes regarding the impactt of the threat event if it occurs.
    additional_mitigation = models.TextField(
        blank=True, help_text=('Are there other opportunites to prevent the threat event'),)  # Kept to determine other areas of improvment that could performed.
    defined1 = models.CharField(
        max_length=128, blank=True, help_text=('Custom defined field for the company '),)  # Used for the custom entry field that may be captured for the client.
    defined2 = models.CharField(
        max_length=128, blank=True, help_text=('Custom defined field for the company '),)  # Used for the custom entry field that may be captured for the client.
    incident_response = models.BooleanField(default=False, help_text=(
        'Is there an incident response plan if the threat event were to happen'),)  # Used to track IR playbooks associated to the threat event.
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='created_entry', help_text=(
        'User id of the user that created the field'),)  # User that created the entry
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='modified_entry', help_text=(
        'User id that last modified the field'),)  # User that last modified the entry
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='deactivated_entry', help_text=(
        'User id if deactivated by another user'),)  # User that deactivated the entry
    entry_owner = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='owner_entry', help_text=(
        ' Who owns management of the risk entry.  This should be a contributor of the system'),)  # User that currently owns and is held accountable for the entry
    register = models.ForeignKey('Register', on_delete=models.PROTECT, null=True, related_name='entry', help_text=(
        'Register that the entry belongs'),)  # Register that the entry is associated.
    response = models.ForeignKey('Response', on_delete=models.CASCADE, null=True, blank=True, related_name='entryfinalresponse', help_text=(
        'The final decsion on what to do with the threat scenario'),)  # Based on the decision from the EntryRespons and EntryResponseResults.  This is what the company has determined to do about the threat scenario.
    actors = models.ManyToManyField('Actor', through='EntryActor',
                                    through_fields=('id_entry', 'id_actor'), related_name='EntryActors', help_text=('Specifies what actors are defined in the scenario'),)  # Many actors could be involved in the threat scenario.
    events = models.ManyToManyField('EventType', through='EntryEventType',
                                    through_fields=('id_entry', 'id_eventtype'), related_name='EntryEvents', help_text=('Specifies what events are used in the threat scenario'),)  # Many events could be involved in the threat scenario.
    assets = models.ManyToManyField('CompanyAsset', through='EntryCompanyAsset', through_fields=('id_entry', 'id_companyasset'), related_name='EntryCompanyAssets', help_text=(
        'Specifies what assets are defined in the scenario'),)  # Many assets could be involved in the threat scenario.
    controls = models.ManyToManyField('CompanyControl', through='EntryCompanyControl', through_fields=('id_entry', 'id_companycontrol'), related_name='EntryCompanyControls', help_text=(
        'Specifies what controls are defined to mitigate against the risk scenario'),)  # Many controls could be used to mitigate risk.
    compliances = models.ManyToManyField('Compliance', through='EntryCompliance', through_fields=('id_entry', 'id_compliance'), related_name='EntryComplianceRequirements', help_text=(
        'Specifies what requirements are associated with the entry'),)  # Compliance requirements may be associated with the risk.
    locations = models.ManyToManyField('CompanyLocation', through='EntryCompanyLocation', through_fields=('id_entry', 'id_companylocation'), related_name='EntryCompanyLocations', help_text=(
        'Specifies what company locations are associated with the entry'),)  # If no locations are specified, it should be ALL locations.
    risk_types = models.ManyToManyField('RiskType', through='EntryRiskType', through_fields=('id_entry', 'id_risktype'), related_name='EntryRiskTypes', help_text=(
        'Specifies business risk types are associated with the entry'),)  # The entry can be associated to more than on risk type
    addtional_mitigation = models.TextField(
        blank=True, null=True, help_text=('Used to provide context on additional mitigation thoughts from the contributor'),)  # Used to provide context on additional mitigation thoughts from the contributor.

    class Meta:
        """Meta class."""

        ordering = ['entry_number']
        indexes = [
            models.Index(fields=['summary'], name='summary_idx'), ]
        verbose_name_plural = ("Entries")
        unique_together = (('register', 'entry_number'),)

    def __str__(self):
        """String."""
        return self.summary

    @property
    def severity(self):
        """Severity calculated with formula (24 ((entryid)-1)) /(maxrevenueloss)."""
        try:
            severity = (24 * (self.id - 1) /
                        self.register.company.annual_revenue)
        except:
            severity = 0
        return severity

    @property
    def mitigation_rate(self):
        """A percentage based formula generated from other items in the application."""
        try:
            entry_control = EntryCompanyControl.objects.get(id_entry=self)
            mitigation_rate = entry_control.mitigation_rate
        except:
            mitigation_rate = round((.78) - (.56), 2)

        return mitigation_rate

    @property
    def has_response(self):
        """Is there a response associated with this."""
        try:
            response = 1 if self.entryresponse.count() else 0
        except:
            response = 0
        return response

    @property
    def impact(self):
        """Is there a response associated with this."""
        try:
            impact = self.entryimpact.latest('id').impact_type_id
        except:
            impact = ''
        return impact

    @property
    def has_compliance(self):
        """Is there a compliance associated with this."""
        try:
            compliance = 1 if self.entrycompliance.count() else 0
        except:
            compliance = 0
        return compliance

    def get_summary(self, length=20):
        """Up to x number of characters with an ellipses if the entry is longer that allowed."""
        return (self.summary[:length] + '...') if len(self.summary) > length + 3 else self.summary

    @property
    def evaluation(self):
        """Evaluation."""
        return self.entryevaluation.order_by('-date_evaluated').first()

    @property
    def date_evaluated(self):
        """Date of valuation."""
        try:
            return self.entryevaluation.order_by('-date_evaluated').first().date_evaluated
        except:
            return ''

    @property
    def total_asset_value(self):
        """Company Assets."""
        total = 0
        for asset_entry in self.companyasset_entry.select_related('id_companyasset').all():
            total += asset_entry.get_asset_value()
        return total

    @property
    def total_control_mitigation(self):
        """Company Control."""
        entry_control = self.companycontrol_entry.order_by('-id').first()
        if entry_control:
            return self.total_asset_value * entry_control.mitigation_rate
        else:
            return 0


class EntryTask(models.Model):
    """Entry Task.  This task will be managed by the entry owner."""

    summary = models.CharField(
        max_length=128, blank=False, help_text=('Brief description of the entry'),)  # Summary of the task for the entry
    desc = models.TextField(
        blank=False, help_text=('Description broader description of the task'),)  # More context for the task
    due_date = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp of the task due date'),)  # Used to determine when the task is due.  Due dates my trigger an alert for the user if past due.
    internal_ticket = models.CharField(
        max_length=45, blank=True, help_text=('Internal ticket associated with the task'),)  # Used if ticket tracking is handled in another system.  // may be used by API for task automation.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the entry task was created'),)  # Date the task was created
    date_completed = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the entry task was closed'),)  # Date the task was completed
    date_acknowledged = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the entry task was acknowledged by the user'),)  # When acknowledged the task status will change to In Progress.
    # Foreign Key and Relationships
    task_owner = models.ForeignKey('CompanyContact', on_delete=models.CASCADE, null=True, related_name='entrytask', help_text=(
        ' Who owns the task'),)  # Task owner may be different from the user the that owns the entry.
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='created_entrytask', help_text=(
        'User id of the user that created the field'),)
    closed_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='closed_entrytask', help_text=(
        'User id of the user that created the field'),)
    deleted_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='deleted_entrytask', help_text=(
        'User id if deleted by another user'),)
    task_status = models.ForeignKey('TaskStatus', on_delete=models.CASCADE, default=1, null=True, related_name='entrytask_status', help_text=(
        'Current status of the task'),)
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entrytask', help_text=(
        'Entry that the registery is tied '),)

    class Meta:
        """Meta class."""

        ordering = ['due_date']
        indexes = [
            models.Index(fields=['summary'], name='summary_idx'), ]
        verbose_name_plural = ("Entry Tasks")

    def __str__(self):
        """String."""
        return self.summary


class EntryCause(models.Model):
    """Entry Cause.   Needs to be reviewed for logic at the entry level.   Maybe a finding cause?"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the cause'),)  # Not in use
    desc = models.TextField(
        blank=False, help_text=('Description of the cause'),)  # Not in use
    keywords = models.TextField(
        blank=True, null=True, help_text=('Keywords used to idenify proper category or find correct field name'),)  # Not in use
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
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entrycause', help_text=(
        'The entry the associated with the cause'),)

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Cause")


class EntryActor(models.Model):
    """Entry Actor.  Use to associate many threat actors and the specific intentions and motives against the assets of the entry."""

    # Entry Id from the Entry table
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, related_name='actor_entry', help_text=(
        'The entry associated to the actor'),)  # Id of the entry
    id_actor = models.ForeignKey('Actor', on_delete=models.CASCADE, related_name='entry_actor', help_text=(
        'The actor associated to the entry'),)  # Id of the actor
    # Context to understand why the actor is tied to the entry
    detail = models.TextField(blank=True, help_text=(
        'Additional detail the actor associated with the threat scenario.'),)
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the actor is active in the threat scenario'),)  # When builing a threat scenario, there may be many actors that need to be considered.
    intentions = models.ManyToManyField("ActorIntent", through='EntryActorIntent',
                                        through_fields=('id_entryactor', 'id_actorintent'), related_name='EntryActorIntentions', help_text=('Common intentions of the Threat Actor for the assoicated entry'),)  # This will be used for reporting and insight content.  It will tie the threat actor to what they intend to do with the asset.
    motives = models.ManyToManyField("ActorMotive", through='EntryActorMotive',
                                     through_fields=('id_entryactor', 'id_actormotive'), related_name='EntryActorMotive', help_text=('Common motives of the Threat Actor for the associated entry'),)  # This will be used for reporting and insight content.  It will tie the threat actor to reason they want the asset.

    def __str__(self):
        """String."""
        return self.id_actor.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Actors")


class EntryActorIntent(models.Model):
    ''' This table is used to tie threat actors to their intent.  '''
    id_entryactor = models.ForeignKey(
        'EntryActor', on_delete=models.CASCADE, related_name='intent_entryactor', help_text=(
            'The actor chosen for the threat scenario'),)  # )  # EntryActor Id from the EntryActor table
    # ActorIntent Id from the ActorIntent table
    id_actorintent = models.ForeignKey('ActorIntent', on_delete=models.CASCADE, related_name='entry_actorintent', help_text=(
        'The intent chosen for the threat scenario'),)
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the entry threat actor intent is active'),)  # There are default intentions for every actor, however this can be specified if needed.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Date the intent was tied to the threat actor'),)  # Date intent was tied to the actor
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='UserCreatedEntryActorIntent', help_text=(
        'User id of the user that created the access'),)
    date_revoked = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the intent tied to the threat actor was revoked, if applicable'),)  # Date actor intent was revoked.
    revoked_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='UserRevokedEntryActorIntent', help_text=(
        'User id that revoked the intent from the threat actor'),)  # User id of the user that revoked the intent from the entry

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Actor Intentions")


class EntryActorMotive(models.Model):
    ''' This table is used to tie threat actors to their motive.  '''
    id_entryactor = models.ForeignKey(
        'EntryActor', on_delete=models.CASCADE, related_name='motive_entryactor', help_text=(
            'The actor chosen for the threat scenario'),)  # )  # EntryActor Id from the Entry Actor table
    # ActorMotive Id from the ActorMotive table
    id_actormotive = models.ForeignKey('ActorMotive', on_delete=models.CASCADE, related_name='entry_actormotive', help_text=(
        'The motive chosen for the threat scenario'),)  # The motive tied to the actor for the entry.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the etry threat actor motive is active'),)  # There defualt motives for every actor, however this can be specified if needed.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Date the motive was tied to the threat actor'),)  # Date the motive was created
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='UserCreatedEntryActorMotive', help_text=(
        'User id of the user that created the threat actor motive'),)
    date_revoked = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the motive tied to the threat actor was revoked, if applicable'),)  # Date threat actor motive was revoked.
    revoked_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='UserRevokedEntryActorMotive', help_text=(
        'User id that revoked the motive from the threat actor'),)  # User id  that revoked the motive from the entry threat actor

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Actor Motives")


class EntryCompanyAsset(models.Model):
    """Entry Company Assets.  Defines the assets associated with the risk entry."""

    # Entry Id from the Entry table
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, related_name='companyasset_entry', help_text=(
        'The entry associated to the actor'),)  # Id of the entry
    id_companyasset = models.ForeignKey('CompanyAsset', on_delete=models.CASCADE, related_name='entry_companyasset', help_text=(
        'The asset associated to the entry'),)  # Id of the asset
    exposure_percentage = models.FloatField(default=1, blank=True, help_text=(
        'Maximum percentage of asset value exposed given the risk scenario'),)  # Based on the value of the asset, this is exposed amount used to determine mitigation impact when controls are applied.  If controls already exist on the entry and a new asset is added to the threat secenario, control review must be performed again.
    detail = models.TextField(blank=True, help_text=(
        'Additional detail the asset associated with the threat scenario.'),)  # Context to understand why the asset is tied to the entry
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the asset is active in the threat scenario'),)  # When builing a threat scenario, there may be many assets that need to be considered.

    def __str__(self):
        """String."""
        return self.id_companyasset.name

    class Meta:
        """Meta class."""

        verbose_name_plural = ("Entry Company Assets")

    def get_asset_value(self):
        """Get the asset value."""
        if self.id_companyasset.monetary_value_toggle:
            # / 100.0
            return (self.id_companyasset.fixed_monetary_value * self.exposure_percentage)
        else:
            # / 100.0
            return (self.id_companyasset.par_monetary_value * self.exposure_percentage)


class EntryCompanyControl(models.Model):
    """Entry Company Control."""

    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.CASCADE, null=True, related_name='entry_companycontrol', help_text=(
        'The company control assigned to mitigate the risk'),)
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='companycontrol_entry', help_text=(
        'The entry the associated with the company control'),)
    mitigation_rate = models.FloatField(default=0, blank=True, help_text=(
        'Percentage of mitigations the control applies to the inherit risk'),)  # Each control added to the entry should mitigate a portion of the over inherit risk. When selecting the mitigation percentage, it should remove the exposed inhert risk from the asset exposure.
    notes = models.TextField(
        blank=True, help_text=('Notes regarding the controls mitigation against the risk'),)  # Notes should be used to suppor the logical leverage to mitigate risk.
    url = models.URLField(max_length=200, blank=True, help_text=(
        'Websites or locations of data supporting the controls mitigation against the risk'),)  # In addtion to notes.  Users can leverage websites for reference.
    submitted_mitigation = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='userlastsubmittedmitigation', help_text=(
        'User id of the user that last submitted mitigation'),)  # This will be the same for all company controls on the entry.  It is captured to understand the last user that submitted values for the control mitigations.
    operation = models.ForeignKey('ControlOperation', on_delete=models.CASCADE, blank=True, null=True, related_name='operation_controlentry', help_text=(
        'The operation associated to the control entered'),)  # Control categories can have multiple operation levels.  This field is used show what may be available for the control and tie its operational level to the entry
    functions = models.ManyToManyField("ControlFunction", through='EntryCompanyControlFunction', through_fields=('id_entrycompanycontrol', 'id_controlfunction'), related_name='EntryCompanyControlFunction', help_text=(
        'The level at which the control functions for the entry'),)  # Control categories can have multiple functions.  This field is used show what may be available for the control.
    measurements = models.ManyToManyField("CompanyControlMeasure", through='EntryCompanyControlMeasure', through_fields=('id_entrycompanycontrol', 'id_companycontrolmeasure'), related_name='EntryCompanyControlMeasurements', help_text=(
        'The measurements related to the threat scenario for this entry'),)  # This will be all or a subset of the measurements for the company control.
    dependencies = models.ManyToManyField("CompanyControlDependency", through='EntryCompanyControlDependency', through_fields=('id_entrycompanycontrol', 'id_companycontroldependency'), related_name='EntryCompanyControlDependencies', help_text=(
        'The dependencies of the control for the entry'),)  # This will be all or a subset of the dependencies for the company control.

    def __str__(self):
        """String."""
        return self.id_companycontrol.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Company Controls")


class EntryCompliance(models.Model):
    """Entry Compliance."""

    # Foreign Key and Relationships
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entrycompliance', help_text=(
        'The entry the associated with the company control'),)
    id_compliance = models.ForeignKey('Compliance', on_delete=models.CASCADE, null=True, related_name='entrycompliance', help_text=(
        'The compliance or regulation associated with the entry'),)

    def __str__(self):
        """String."""
        return self.id_compliance.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Compliance")


class EntryRiskType(models.Model):
    """Entry Risk Type."""

    # Foreign Key and Relationships
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entryrisktype', help_text=(
        'The entry the associated with the risk type'),)
    id_risktype = models.ForeignKey('RiskType', on_delete=models.CASCADE, null=True, related_name='risktypeentry', help_text=(
        'The business risk type associated with the entry'),)

    def __str__(self):
        """String."""
        return self.id_risktype.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Risk Types")


class EntryCompanyControlFunction(models.Model):
    """Entry Company Control Function.  When chosing this list it should control functions should be limited by what is available for the control category."""

    # Foreign Key and Relationships
    id_controlfunction = models.ForeignKey('ControlFunction', on_delete=models.CASCADE, null=True, related_name='entry_controlfunction', help_text=(
        'The function the control preforms against the threat event'),)
    id_entrycompanycontrol = models.ForeignKey('EntryCompanyControl', on_delete=models.CASCADE, null=True, related_name='controlfunction_entry', help_text=(
        'The entry control the associated with the company control'),)

    def __str__(self):
        """String."""
        return self.id_controlfunction.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Company Control Functions")


class EntryCompanyControlMeasure(models.Model):
    """Entry Control Measure."""

    # Foreign Key and Relationships
    id_companycontrolmeasure = models.ForeignKey('CompanyControlMeasure', on_delete=models.CASCADE, null=True, related_name='entry_companycontrolmeasure', help_text=(
        'The measurement for the company control used on the threat scenario'),)
    id_entrycompanycontrol = models.ForeignKey('EntryCompanyControl', on_delete=models.CASCADE, null=True, related_name='companycontrolmeasure_entry', help_text=(
        'The entry associated with the company control'),)

    def __str__(self):
        """String."""
        return self.id_companycontrolmeasure.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Company Control Measures")


class EntryCompanyControlDependency(models.Model):
    """Entry Control Dependency."""

    # Foreign Key and Relationships
    id_companycontroldependency = models.ForeignKey('CompanyControlDependency', on_delete=models.CASCADE, null=True, related_name='entry_companycontroldependency', help_text=(
        'The dependency for the company control used on the threat scenario'),)
    id_entrycompanycontrol = models.ForeignKey('EntryCompanyControl', on_delete=models.CASCADE, null=True, related_name='companycontroldependency_entry', help_text=(
        'The entry associated with the company control'),)

    def __str__(self):
        """String."""
        return self.id_companycontroldependency.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Company Control Dependencies")


class EntryEvaluation(models.Model):
    """Entry Evaluation."""

    update = models.TextField(
        blank=True, help_text=('Notes regarding the evaluation'),)  # Updates to the evaluation if any were created.
    date_created = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the evaluation event triggered'),)  # Date the evaluation triggered
    date_evaluated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the risk entry was evaluated'),)  # Date the user completed submitted the evaluation
    # Foreign Key and Relationships
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entryevaluation', help_text=(
        'The entry the associated with the evaluation'),)  # Evaluation entry
    mitigation_adequacy = models.ForeignKey('MitigationAdequacy', on_delete=models.CASCADE, null=True, related_name='entrymitigation', help_text=(
        'Mitigation level based on infromation available'),)  # Is the control mitigation adequate for the risk based on the users perception.
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='entryevaluation', help_text=(
        'The user that performed the evaluation'),)  # User that completed the evaluation.

    def __str__(self):
        """String."""
        return self.notes

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Evaluations")


class EntryEventType(models.Model):
    """Entry Event Type.  Define the event that is being mitigated."""

    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='eventtype_entry', help_text=(
        'The entry the associated with the company control'),)
    id_eventtype = models.ForeignKey('EventType', on_delete=models.CASCADE, null=True, related_name='entry_eventtype', help_text=(
        'Type of event associated to the threat event'),)
    context = models.TextField(
        blank=True, help_text=('Context to the event for the entry'),)  # Additional information may be needed to understand why the eventtype is being used for the threat scenario.

    def __str__(self):
        """String."""
        return self.id_eventtype.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Event Types")


class EntryImpact(models.Model):
    """Entry Impact."""

    fixed_cost = models.DecimalField(null=True, blank=True, max_digits=30, decimal_places=2, help_text=(
        'The fixed monetary loss the impact would have if triggered'),)  # This is fixed cost of a single instance.  Monetary_value_toggle = False.  Used determine logic regarding impact and cost.  Will be multipled by the frequency.
    pml_cost = models.FloatField(null=True, blank=True, help_text=(
        'Percentage of max loss the impact would cost if triggered'),)  # This is the percentage of the maxium loss the company can have annually.  Monetary_value_toggle = True.  Used determine logic regarding impact and cost. will be multipled by the frequency.
    monetary_value_toggle = models.BooleanField(
        default=False, help_text=('Toggle to determine if the impact cost is measured by fixed=False or pml =True monetary value'),)  # If False, use Fixed cost for calculations.  If True, use PML cost for calculations.
    notes = models.TextField(
        blank=True, help_text=('Notes regarding the impact has for the impact'),)  # Not in use
    # Foreign Key and Relationships
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entryimpact', help_text=(
        'The entry the associated with the entry impact'),)
    impact_type = models.ForeignKey('ImpactType', on_delete=models.CASCADE, null=True, related_name='entryimpact', help_text=(
        'Impact type for the risk entry'),)

    def __str__(self):
        """String."""
        return self.percent

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Impact")


class EntryIndicator(models.Model):
    """Entry Indicator."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the indicator'),)  # Not in use
    desc = models.TextField(
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
    example_image1 = models.ImageField(
        help_text=('Image used to support context for example 1'), null=True, blank=True,)  # Not in use
    example_image2 = models.ImageField(
        help_text=('Image used to support context for example 2'), null=True, blank=True,)  # Not in use
    desc_alt = models.CharField(
        max_length=100, blank=True, null=True, help_text=('Alternate description used for image and text hover'),)  # Not in use
    desc_form = models.CharField(
        max_length=200, blank=True, null=True, help_text=('Form verbiage used for form inputs by the user'),)  # Not in use

    # Foreign Key and Relationships
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entryindicator', help_text=(
        'The entry the associated with the entry impact'),)

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Indicators")


class EntryCompanyLocation(models.Model):
    """
    Entry Company Location.

    This model ties the register entry to a specific location for the
    client.  If nothing is defined, then all locations.
    """

    # Foreign Key and Relationships
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entry_companylocation', help_text=(
        'The entry the associated with company location'),)
    id_companylocation = models.ForeignKey('CompanyLocation', on_delete=models.CASCADE, null=True, related_name='companylocation_entry', help_text=(
        'Company location that the risk entry applies'),)

    def __str__(self):
        """String."""
        return self.id_companylocation.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Company Locations")


class EntryResponse(models.Model):
    """
    Entry Response.

    This model is used to determine how the company will handle the risk and
    who owns response for the risk.
    """

    date_presented = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the entry was presented for response'),)  # Used to determine when the threat scenario was presented to decision makers
    date_decision = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the decision was made on how to handle the risk entry'),)  # Used to determine when a decision was made on the threat scenario.
    justification = models.TextField(
        blank=False, help_text=('Description of the response justification'),)  # Context to the logic of the decision being made.
    budget = models.DecimalField(default=0, blank=True, max_digits=30, decimal_places=2, help_text=(
        'Budget allocated to support threat event'),)  # Used to define the budget needed for the threat scenario.
    date_target = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Target date to complete the response objective.  ie complete treatment date'),)  # Date targeted to complete the needed mitigation.
    notes = models.TextField(
        blank=True, help_text=('Notes regarding the response decision'),)  # Additional information for the risk scenario.
    # Foreign Key and Relationships
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entryresponse', help_text=(
        'The entry the associated with the entry impact'),)  # There may be more that one review of the entry as time changes.  This will provide the historic content.
    suggested_response = models.ForeignKey('Response', on_delete=models.CASCADE, null=True, blank=True, related_name='entrysuggestedresponse', help_text=(
        'The suggested response on what to do with the threat scenario'),)
    response_votes = models.ManyToManyField("CompanyContact", through='EntryResponseResult',
                                            through_fields=('id_entryresponse', 'id_decisionmaker'), related_name='EntryResponseResult', help_text=('Shows the Decision Makers and their response'),)  # This provides information on who/how someone voted for the response on the threat scenario.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Responses")


class EntryResponseResult(models.Model):
    """
    Entry Response Result.  This allows users to provide their approval or deny on the response for the threat scenario.  Used to support the result of the response.  May also be used to let decison makers vote within the application based on a timeline.
    """

    # Foreign Key and Relationships
    id_entryresponse = models.ForeignKey('EntryResponse', on_delete=models.CASCADE, null=True, related_name='entryresponse_decisionmaker', help_text=(
        'The entry associated with decisionmaker response (vote)'),)
    id_decisionmaker = models.ForeignKey('CompanyContact', on_delete=models.CASCADE, null=True, related_name='decisionmaker_entry', help_text=(
        'The decisionmaker that the risk entry response applies'),)
    vote_status = models.ForeignKey('ResponseVote', on_delete=models.CASCADE, default=1, related_name='entryresponsevote', help_text=(
        'The vote cast by the decision maker'),)  # The vote cast by the decison maker
    vote_response = models.ForeignKey('Response', on_delete=models.CASCADE, null=True, blank=True, related_name='entryresponseresultvote', help_text=(
        'The suggested vote the decision maker made for the threat scenario'),)
    notes = models.TextField(
        blank=True, help_text=('Notes regarding the decison makers vote'),)

    def __str__(self):
        """String."""
        return self.vote_response.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Response Votes")


class ResponseVote(models.Model):
    """Response Vote."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the response'),)  # Name of the response
    desc = models.TextField(
        blank=False, help_text=('Description of the repsonse'),)  # Description of the response
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed to the user'),)  # Used when presenting a selection to contributors

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Response Votes")


class Response(models.Model):
    """Response."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the response'),)  # Not in use
    desc = models.TextField(
        blank=False, help_text=('Description of the repsonse'),)  # Not in use
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed to the user'),)  # Not in use
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


class EntryUrl(models.Model):
    """Entry Url."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the URL'),)  # Name of the URL
    notes = models.TextField(
        blank=False, help_text=('Notes on why the url was selected for the entry'),)  # Notes associated with the URL
    url = models.URLField(max_length=512, blank=True, help_text=(
        'URL used to support detail of the entry'),)  # Website or URL of the location defined.
    is_internal = models.BooleanField(
        default=False, help_text=('Designates whether the URL is internal to the company'),)  # If true, the URL is only accessable to company users.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the URL is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the URL is no longer associated with the entry.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the URL was created'),)  # User that added the URL
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the URL was deactivated'),)  # Date the URL was removed
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='created_entryurl', help_text=(
        'User id of the user that created the field'),)  # User that created the URL
    deactivated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='deactivated_entryurl', help_text=(
        'User that deactivated the URL'),)  # User that deactivated the URL
    # RLB Processing
    date_scanned = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the URL was last scanned'),)  # Date the URL was last scanned by RLB processing.  Timestamp will be used to randomly test availability.
    is_public = models.BooleanField(
        default=False, help_text=('Designates whether the URL is publically accessible'),)  # RLB processing has found the URL is publically accessible.
    has_page_error = models.BooleanField(
        default=False, help_text=('Designates whether the URL recieves a page error'),)  # If is_public_domain is True after scan then has_page_error will be tested.  If has_page_error is True, then manual review is needed and alert will be sent to entry owner.
    is_recommended = models.BooleanField(
        default=False, help_text=('Designates whether the URL is recommended by RLB'),)  # URL has been reviewed by RLB and is recommend for this type of entry.
    recommended_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='user_recommended', help_text=(
        'User that recommended the URL'),)  # User that recommended the URL
    recommended_notes = models.TextField(
        blank=True, help_text=('Notes on why the url was recommended reading for other RLB users'),)  # Recommendation notes associated with the URL
    # Foreign Key and Relationships
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entryurl', help_text=(
        'The entry the associated with the entry impact'),)

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry URL")


class RiskType(models.Model):
    """Risk Type.   The type of business risk assocated to the threat scenerio"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the business risk type'),)  # The name of the risk type
    desc = models.TextField(
        blank=False, help_text=('Description of the business risk'),)  # The description of the risk type.
    results = models.TextField(
        blank=True, help_text=('Resulting behaviour'),)  # Results that occur with the risk type happens.
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct risk type'),)  # Keywords used with the risk
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
        'Account', default=1, related_name='account_risktype', on_delete=models.PROTECT, help_text=('The account that the risk type is related'),)  # Companies may have the ability to add their own risk types name.  These will be under review for addtion to CORE.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Risk Types")


class MitigationAdequacy(models.Model):
    """Mitigation Adequacy.  This best defines the mitigation state."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of how adequate the mitigation is defined'),)  # Name of the mitigation adequacy
    desc = models.TextField(
        blank=False, help_text=('Description of how adequate the mitigation is defined'),)  # Description of the mitigation adequacy
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
        verbose_name_plural = ("Mitigation Adequacy")

    def __str__(self):
        """String."""
        return self.name
