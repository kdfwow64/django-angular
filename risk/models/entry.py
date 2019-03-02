"""Register Entries & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
    DefaultFieldsContext,
)


class Register(DefaultFields):
    """Register.  Primary register that holds all entries."""

    NAME_CHOICES = (
        ('primary', 'Primary'),
        ('demo', 'Demo'),
        ('backup', 'Backup'),
    )
    # Used to determine how the cost is classifed for accounting purposes.
    name = models.CharField(
        max_length=14, choices=NAME_CHOICES, default='primary', blank=False, help_text=('Name of the company register '),)  # Name of the company register. There should only be 1 register per company, however special circumstances may require addtional registers such as transition, backup, demo, etc.
    entry_number_queue = models.IntegerField(
        default=1, help_text=('The entry number that is displayed to the contributor specific to the company register'),)  # Each company register will have its own numbering increment process based on this number. 1,2,3,etc.  Each time an entry is created the number will be incremented so it looks as though the numbering is specific to the company.
    company = models.ForeignKey('Company', on_delete=models.PROTECT, blank=False, related_name='company_register', help_text=(
        'Company id for the register.'),)  # Company that the register is associated.

    class Meta:
        """Meta class."""

        ordering = ['company', 'name']
        unique_together = (('name', 'company'),)

    def __str__(self):
        """String."""
        return "{}- {}" .format(self.company, self.name)


class Entry(DefaultFields):
    """Entry."""

    summary = models.CharField(
        max_length=128, blank=False, help_text=('Brief description of the risk'),)  # Brief summary of the risk to be tracked.  Specifically used when listing entries.
    description = models.TextField(
        blank=False, help_text=('Broader description of the registery entry'),)  # More content to provide a better understanding of the risk.
    assumption = models.TextField(
        blank=True, null=True, help_text=('Assumptions made when defining the entry'),)  # There may be assumptions made for the entry.  This provides more insight on how the entry will be managed.
    entry_number = models.IntegerField(
        blank=True, null=True, help_text=('The number that is displayed to the client for the register'),)  # This is the number viewable to the user.  The companies should not see the actual entry id in the application.  Logic will need to be used to identify the lastest value in the "entry_number_queue" from the Register Model.
    is_completed = models.BooleanField(
        default=False, help_text=('Designates whether the entry is complete'),)  # Only entries that are listed as completed can be leveraged for risk reporting.
    date_completed = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the entry was completed'),)  # This is the date the entry can be leveraged for risk reporting.
    mitigation_notes = models.TextField(
        blank=True, null=True, help_text=('Notes regarding the logic for the mitigation'),)  # Notes regarding the impactt of the threat event if it occurs.
    additional_mitigation = models.TextField(
        blank=True, null=True, help_text=('Are there other opportunites to prevent the threat event'),)  # Kept to determine other areas of improvment that could performed.
    defined1 = models.CharField(
        max_length=128, blank=True, help_text=('Custom defined field for the company '),)  # Used for the custom entry field that may be captured for the client.
    defined2 = models.CharField(
        max_length=128, blank=True, help_text=('Custom defined field for the company '),)  # Used for the custom entry field that may be captured for the client.
    incident_response = models.BooleanField(default=False, help_text=(
        'Is there an incident response plan if the threat event were to happen'),)  # Used to track IR playbooks associated to the threat event.
    evaluation_days = models.IntegerField(blank=True, null=True,
                                          help_text=('Defines the default number of days an evaluation should occur'),)  # Default value for field should be pulled from the Company.evaluation_days value.
    evaluation_flg = models.BooleanField(
        default=False, help_text=('Defines if an evaluation is due for the asset'),)  # If True, evaluation is needed.
    aro_toggle = models.CharField(choices=Selector.ARO, default='K', max_length=1, help_text=(
        'Toggle to determine how the ARO is calculated'),)
    aro_notes = models.TextField(
        blank=True, help_text=('Additional notes from the contributor regarding the frequency calculation.'),)  # Notes regarding the frequency of the threat event
    # This used to determine the number of times annual the risk may occur.
    # Logic in the application will be used to set the number
    aro_fixed = models.DecimalField(default=1, max_digits=19, decimal_places=10, help_text=(
        'Fixed number of occurrences on an annual basis to determine total frequency per year.'),)
    aro_known_multiplier = models.FloatField(
        blank=True, default=1, help_text=('The number of times per time unit.'),)  # The user will select the number of times per aro_unit the threat scenario may occur.  This will define the ARO value and provide every x number of aro_known_time_quantity days.
    aro_known_unit_quantity = models.IntegerField(
        default=1, blank=True, help_text=('Defines the number of time units chosen'),)
    # Foreign Key and Relationships
    aro_time_unit = models.ForeignKey(
        'TimeUnit', on_delete=models.PROTECT, default=6, null=True, related_name='entry_aro_unit', help_text=('Cadence used on a know occurance'),)  # This setting combined with aro_known_quantity will define the number of times the event occurs.
    aro_frequency = models.ForeignKey(
        'FrequencyCategory', on_delete=models.PROTECT, blank=True, null=True, related_name='entry_aro_frequency', help_text=('Frequency Category used to help define ARO'),)  # This setting combined with leveages the average of maximum and minimum values of the frequecy category chosen to determine estimated ARO.  This will also be used for reporting items that are generalized versus having a though out value.
    entry_owner = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='owner_entry', help_text=(
        ' Who owns management of the risk entry.  This should be a contributor of the system'),)  # User that currently owns and is held accountable for the entry
    register = models.ForeignKey('Register', on_delete=models.PROTECT, null=True, related_name='entry', help_text=(
        'Register that the entry belongs'),)  # Register that the entry is associated.
    response = models.ForeignKey('Response', default=6, on_delete=models.CASCADE, null=True, blank=True, related_name='entry_response', help_text=(
        'The final decsion on what to do with the threat scenario'),)  # Defines how the company will manage the risk
    actors = models.ManyToManyField('Actor', through='EntryActor',
                                    through_fields=('id_entry', 'id_actor'), related_name='EntryActors', help_text=('Specifies what actors are defined in the scenario'),)  # Many actors could be involved in the threat scenario.
    events = models.ManyToManyField('EventType', through='EntryEventType',
                                    through_fields=('id_entry', 'id_eventtype'), related_name='EntryEvents', help_text=('Specifies what events are used in the threat scenario'),)  # Many events could be involved in the threat scenario.
    assets = models.ManyToManyField('CompanyAsset', through='EntryCompanyAsset', through_fields=('id_entry', 'id_companyasset'), related_name='EntryCompanyAssets', help_text=(
        'Specifies what assets are defined in the scenario'),)  # Many assets could be involved in the threat scenario.
    controls = models.ManyToManyField('CompanyControl', through='EntryCompanyControl', through_fields=('id_entry', 'id_companycontrol'), related_name='EntryCompanyControls', help_text=(
        'Specifies what controls are defined to mitigate against the risk scenario'),)  # Many controls could be used to mitigate risk.
    compliances = models.ManyToManyField('Compliance', through='EntryCompliance', through_fields=('id_entry', 'id_compliance'), related_name='EntryCompliances', help_text=(
        'Specifies what requirements are associated with the entry'),)  # Compliance requirements may be associated with the risk.
    compliance_requirements = models.ManyToManyField('ComplianceRequirement', through='EntryComplianceRequirement', through_fields=('id_entry', 'id_compliance_requirement'), related_name='EntryComplianceRequirements', help_text=(
        'Specifies what requirements are associated with the entry'),)  # Compliance requirements may be associated with the risk.
    locations = models.ManyToManyField('CompanyLocation', through='EntryCompanyLocation', through_fields=('id_entry', 'id_companylocation'), related_name='EntryCompanyLocations', help_text=(
        'Specifies what company locations are associated with the entry'),)  # If no locations are specified, it should be ALL locations.
    risk_types = models.ManyToManyField('RiskType', through='EntryRiskType', through_fields=('id_entry', 'id_risktype'), related_name='EntryRiskTypes', help_text=(
        'Specifies business risk types are associated with the entry'),)  # The entry can be associated to more than on risk type
    artifacts = models.ManyToManyField('CompanyArtifact', through='EntryCompanyArtifact', through_fields=('id_entry', 'id_companyartifact'), related_name='EntryCompnayArtifacts', help_text=(
        'The files that provide context to the entry inputs'),)  # This will link the entry to files uploaded for documentation and support.  The artifact files should reside in risk/ uploads/<company.id>/artifacts/filename.ext

    class Meta:
        """Meta class."""

        ordering = ['register', 'entry_number']
        indexes = [
            models.Index(fields=['summary'], name='summary_idx'), ]
        verbose_name_plural = ("Entries")
        unique_together = (('register', 'entry_number'),)

    def __str__(self):
        """String."""
        return self.summary

    @property
    def severity(self):
        """Severity calculated with test formula (24 ((entryid)-1)) /(maxrevenueloss)."""
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
            response = 1 if self.entryresponsesubmission.count() else 0
        except:
            response = 0
        return response

    @property
    def impact(self):
        """Is there impact associated with this."""
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

    def get_summary(self, length=80):
        """Up to x number of characters with an ellipses if the entry is longer that allowed."""
        return (self.summary[:length] + '...') if len(self.summary) > length + 3 else self.summary

    @property
    def evaluation(self):
        """Evaluation."""
        return self.entryevaluation.order_by('-date_evaluated').first()

    @property
    def date_evaluated(self):
        """Date of evaluation."""
        try:
            return self.entryevaluation.order_by('-date_evaluated').first().date_evaluated
        except:
            return ''

    @property
    def total_asset_value(self):
        """Company Assets."""
        total = 0
        for asset_entry in self.companyasset_entry.select_related('id_companyasset').all():
            total += asset_entry.get_entry_asset_value()
        return total

    @property
    def total_control_mitigation(self):
        """Company Control."""
        entry_control = self.companycontrol_entry.order_by('-id').first()
        if entry_control:
            return self.total_asset_value * entry_control.mitigation_rate
        else:
            return 0


class EntryTask(DefaultFields):
    """Entry Task.  This task will be managed by the entry owner."""

    summary = models.CharField(
        max_length=128, blank=False, help_text=('Brief description of the entry'),)  # Summary of the task for the entry
    description = models.TextField(
        blank=False, help_text=('Description broader description of the task'),)  # More context for the task
    due_date = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp of the task due date'),)  # Used to determine when the task is due.  Due dates my trigger an alert for the user if past due.
    internal_ticket = models.CharField(
        max_length=45, blank=True, help_text=('Internal ticket associated with the task'),)  # Used if ticket tracking is handled in another system.  // may be used by API for task automation.
    date_completed = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the entry task was closed'),)  # Date the task was completed
    date_acknowledged = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the entry task was acknowledged by the user'),)  # When acknowledged the task status will change to In Progress.
    # Foreign Key and Relationships
    task_owner = models.ForeignKey('CompanyContact', on_delete=models.CASCADE, null=True, related_name='entrytask', help_text=(
        ' Who owns the task'),)  # Task owner may be different from the user the that owns the entry.
    closed_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='closed_entrytask', help_text=(
        'User id of the user that created the field'),)
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


class EntryCause(DefaultFieldsEntry):
    """Entry Cause.   Needs to be reviewed for logic at the entry level.   Maybe a finding cause?"""

    keywords = models.TextField(
        blank=True, null=True, help_text=('Keywords used to idenify proper category or find correct field name'),)  # Not in use
    # Foreign Key and Relationships

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Cause")


class EntryActor(DefaultFields):
    """Through table for Entry.  Entry Actor.  Use to associate many threat actors and the specific intentions and motives against the assets of the entry."""

    # Entry Id from the Entry table
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, related_name='actor_entry', help_text=(
        'The entry associated to the actor'),)  # Id of the entry
    id_actor = models.ForeignKey('Actor', on_delete=models.CASCADE, related_name='entry_actor', help_text=(
        'The actor associated to the entry'),)  # Id of the actor
    # Context to understand why the actor is tied to the entry
    detail = models.TextField(blank=True, help_text=(
        'Additional detail the actor associated with the threat scenario.'),)
    intentions = models.ManyToManyField("ActorIntent", through='EntryActorIntent',
                                        through_fields=('id_entryactor', 'id_actorintent'), related_name='EntryActorIntentions', help_text=('Common intentions of the Threat Actor for the assoicated entry'),)  # This will be used for reporting and insight content.  It will tie the threat actor to what they intend to do with the asset.
    motives = models.ManyToManyField("ActorMotive", through='EntryActorMotive',
                                     through_fields=('id_entryactor', 'id_actormotive'), related_name='EntryActorMotive', help_text=('Common motives of the Threat Actor for the associated entry'),)  # This will be used for reporting and insight content.  It will tie the threat actor to reason they want the asset.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Actors")

    def __str__(self):
        """String."""
        return self.id_actor.name


class EntryActorIntent(DefaultFields):
    ''' Through table for EntryActor. used to tie threat actors to their intent.  '''
    id_entryactor = models.ForeignKey(
        'EntryActor', on_delete=models.CASCADE, related_name='intent_entryactor', help_text=(
            'The actor chosen for the threat scenario'),)  # )  # EntryActor Id from the EntryActor table
    # ActorIntent Id from the ActorIntent table
    id_actorintent = models.ForeignKey('ActorIntent', on_delete=models.CASCADE, related_name='entry_actorintent', help_text=(
        'The intent chosen for the threat scenario'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Actor Intentions")


class EntryActorMotive(DefaultFields):
    ''' Through table for EntryActor.  used to tie threat actors to their motive.  '''
    id_entryactor = models.ForeignKey(
        'EntryActor', on_delete=models.CASCADE, related_name='motive_entryactor', help_text=(
            'The actor chosen for the threat scenario'),)  # )  # EntryActor Id from the Entry Actor table
    # ActorMotive Id from the ActorMotive table
    id_actormotive = models.ForeignKey('ActorMotive', on_delete=models.CASCADE, related_name='entry_actormotive', help_text=(
        'The motive chosen for the threat scenario'),)  # The motive tied to the actor for the entry.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Actor Motives")


class EntryCompanyAsset(DefaultFields):
    """Through table for Entry.  Entry Company Assets.  Defines the assets associated with the risk entry."""

    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, related_name='companyasset_entry', help_text=(
        'The entry associated to the actor'),)  # Id of the entry
    id_companyasset = models.ForeignKey('CompanyAsset', on_delete=models.CASCADE, related_name='entry_companyasset', help_text=(
        'The asset associated to the entry'),)  # Id of the asset
    exposure_factor_fixed = models.DecimalField(default=0, max_digits=30, decimal_places=2, help_text=(
        'The fixed monetary value of the exposure factor dollars'),)  # The exposure factor may be a fixed cost if the threat scenario is realized.
    exposure_factor_rate = models.FloatField(default=1, blank=True, null=True, help_text=(
        'Maximum percentage of asset value exposed given the threat scenario'),)  # Based on the value of the assets in the threat scenario, this is the amount of exposed value used to determine mitigation impact when controls are applied.  If controls already exist on the entry and a new asset is added to the threat secenario, control review should be performed again.
    exposure_factor_toggle = models.CharField(choices=Selector.EF, default='F', max_length=1,
                                              help_text=('Toggle to determine which formula is used to determine the exposure factor'),)  # Defines which logic to use when generating asset value against the entry threat scenario. This toggle defaults to '1' a percent of asset value.
    detail = models.TextField(blank=True, help_text=(
        'Additional detail the asset associated with the threat scenario.'),)  # Context to understand why the asset is tied to the entry

    class Meta:
        """Meta class."""

        verbose_name_plural = ("Entry Company Assets")

    def __str__(self):
        """String."""
        return self.id_companyasset.name

    def get_entry_asset_sle_value(self):
        """Get the asset value."""
        if self.exposure_factor_toggle == 'P':
            # The contributor has chosen a percentage of the asset value is at
            # risk.
            return (self.id_companyasset.get_asset_value * self.exposure_factor_percent)
        elif self.exposure_factor_toggle == 'F':
                # The contributor has chosen the a fixed monetary amount at
                # risk.
            return (self.exposure_factor_fixed)


class EntryCompanyControl(DefaultFields):
    """Through table for Entry.  Entry Company Control."""

    id_companycontrol = models.ForeignKey('CompanyControl', on_delete=models.CASCADE, null=True, related_name='entry_companycontrol', help_text=(
        'The company control assigned to mitigate the risk'),)
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='companycontrol_entry', help_text=(
        'The entry the associated with the company control'),)
    aro_mitigation_rate = models.FloatField(default=0, blank=True, null=True, help_text=(
        'Rate of mitigation the control applies to the Annual Rate of Occurence'),)  # The percentage of mitigation the control provides to the annual rate of occurence.
    sle_mitigation_rate = models.FloatField(default=0, blank=True, null=True, help_text=(
        'Rate of mitigation the control applies to the SLE'),)  # The percentage of mitigation the control applies to the single loss expectancy
    notes = models.TextField(
        blank=True, help_text=('Notes regarding the controls mitigation against the risk'),)  # Notes should be used to suppor the logical leverage to mitigate risk.
    url = models.URLField(max_length=200, blank=True, help_text=(
        'Websites or locations of data supporting the controls mitigation against the risk'),)  # In addtion to notes.  Users can leverage websites for reference.
    submitted_mitigation = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='userlastsubmittedmitigation', help_text=(
        'User id of the user that last submitted mitigation'),)  # This will be the same for all company controls on the entry.  It is captured to understand the last user that submitted values for the control mitigations.
    alert_method = models.ForeignKey('ControlAlertMethod', on_delete=models.CASCADE, blank=True, null=True, related_name='alertmethod_controlentry', help_text=(
        'The notification ability associated to the control entered'),)  # Control categories can have multiple notification levels.  This field is used show what may be available for the control and tie its notification level to the entry
    cia_triad = models.ManyToManyField('CIATriad', through='EntryCompanyControlCIATriad', through_fields=('id_entrycompanycontrol', 'id_ciatriad'), related_name='EntryCompanyControlCIATriads', help_text=(
        'Specifies what portion of the triad is associated to the control entry'),)  # Ties CIA Triad to the event entry.
    measurements = models.ManyToManyField("CompanyControlMeasure", through='EntryCompanyControlMeasure', through_fields=('id_entrycompanycontrol', 'id_companycontrolmeasure'), related_name='EntryCompanyControlMeasurements', help_text=(
        'The measurements related to the threat scenario for this entry'),)  # This will be all or a subset of the measurements for the company control.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Company Controls")

    def __str__(self):
        """String."""
        return self.id_companycontrol.name


class EntryCompliance(DefaultFields):
    """Through table for Entry.  Entry Compliance."""

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


class EntryComplianceRequirement(DefaultFields):
    """Through table for Entry.  Entry Compliance Requirement."""

    # Foreign Key and Relationships
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entrycompliancerequirement', help_text=(
        'The entry the associated with the company control'),)
    id_compliance_requirement = models.ForeignKey('ComplianceRequirement', on_delete=models.CASCADE, null=True, related_name='entrycompliancerequirement', help_text=(
        'The compliance requirement or regulation associated with the entry'),)

    def __str__(self):
        """String."""
        return self.id_compliancerequirement.requirement

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Compliance Requirements")


class EntryRiskType(DefaultFields):
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


class EntryCompanyArtifact(DefaultFields):
    """Through table for Entry. CompanyArtifactFile."""

    # Foreign Key and Relationships
    id_entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entrycompanyartifact', help_text=(
        'The entry the associated with the company artifact'),)
    id_companyartifact = models.ForeignKey('CompanyArtifact', on_delete=models.CASCADE, null=True, related_name='companyartifactentry', help_text=(
        'The artifact associated with the entry'),)
    entry_note = models.TextField(
        blank=True, help_text=('Note on the artifact specific to the entry'),)  # When the evaluation_flg is set, the reason should be defined.

    def __str__(self):
        """String."""
        return self.id_companyartifact.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Artifacts")


class EntryCompanyControlCIATriad(DefaultFields):
    """Through table for EntryCompanyControl.  Entry Company Control CIATriad  When chosing this list it should be limited by what is available for the control category cia."""

    # Foreign Key and Relationships
    id_ciatriad = models.ForeignKey('CIATriad', on_delete=models.PROTECT, null=True, related_name='entrycompanycontrol_cia', help_text=(
        'The CIA Triad'),)
    id_entrycompanycontrol = models.ForeignKey('EntryCompanyControl', on_delete=models.CASCADE, null=True, related_name='cia_entrycompanycontrol', help_text=(
        'The entry control the associated with the company control'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry: Company Control CIA")


class EntryCompanyControlMeasure(DefaultFields):
    """Through table for EntryCompanyControl.  Entry Control Measure."""

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


class EntryEvaluation(DefaultFields):
    """Entry Evaluation."""

    update = models.TextField(
        blank=True, help_text=('Notes regarding the evaluation'),)  # Updates to the evaluation if any were created.
    request_note = models.TextField(
        blank=True, help_text=('Notes regarding the logic of why the evaluation was requested'),)  # When the evaluation_flg is set, the reason should be defined.
    date_evaluated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the risk entry was evaluated'),)  # Date the user completed submitted the evaluation
    date_approved = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the final approval of the entry'),)  # Date the approver approved the evaluation.
    date_requested = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the reqestor requested the evaluation'),)  # Date the requestor requested the evaluation.
    # Foreign Key and Relationships
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE, null=True, related_name='entry_evaluation', help_text=(
        'The entry the associated with the evaluation'),)  # Evaluation entry
    mitigation_adequacy = models.ForeignKey('MitigationAdequacy', on_delete=models.CASCADE, null=True, related_name='entrymitigation', help_text=(
        'Mitigation level based on infromation available'),)  # Is the control mitigation adequate for the risk based on the users perception.
    evaluator = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='entryevaluation_evaluator', help_text=(
        'The user that performed the evaluation'),)  # User that completed the evaluation.
    approver = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='entryevaluation_approver', help_text=(
        'The user that performed the evaluation'),)  # User that completed the evaluation.
    requestor = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='entryevaluation_requestor', help_text=(
        'The user that requested the evaluation'),)  # User that completed the evaluation.

    def __str__(self):
        """String."""
        return self.notes

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Evaluations")


class EntryEventType(DefaultFields):
    """Through table for Entry.  Entry Event Type.  Define the event that is being mitigated."""

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


class EntryIndicator(DefaultFieldsEntry):
    """Entry Indicator."""

    notes = models.TextField(
        blank=True, null=True,  help_text=('Notes associated wtih the indicator'),)  # Not in use

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Indicators")


class EntryCompanyLocation(DefaultFields):
    """
    Through table for Entry.  Entry Company Location. This model ties the register entry to a specific location for the client.  If nothing is defined, then all locations.
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


class EntryResponseSubmission(DefaultFields):
    """
    Future usage to submit governacce response.  Entry Response.

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
                                            through_fields=('id_entryresponsesubmission', 'id_decisionmaker'), related_name='EntryResponseResult', help_text=('Shows the Decision Makers and their response'),)  # This provides information on who/how someone voted for the response on the threat scenario.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry Response Submission")


class EntryResponseResult(DefaultFields):
    """
    Future usage to submit governacce response.

    Entry Response Result.  This allows users to provide their approval or deny on the response for the threat scenario.  Used to support the result of the response.  May also be used to let decison makers vote within the application based on a timeline.
    """

    id_entryresponsesubmission = models.ForeignKey('EntryResponseSubmission', on_delete=models.CASCADE, null=True, related_name='entryresponsesubmission_decisionmaker', help_text=(
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


class ResponseVote(DefaultFieldsCompany):
    """
    Future usage to submit governacce response.

    Response Vote.

    """

    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed to the user'),)  # Used when presenting a selection to contributors

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Response Votes")

    def __str__(self):
        """String."""
        return self.name


class Response(DefaultFieldsCategory):
    """Response.
    """
    class Meta:
        """Meta class."""
        ordering = ('sort_order',)

    def __str__(self):
        """String."""
        return self.name


class EntryUrl(DefaultFieldsEntry):
    """Entry Url."""

    notes = models.TextField(
        blank=True, null=True, help_text=('Notes on why the url was selected for the entry'),)  # Notes associated with the URL
    url = models.URLField(max_length=512, help_text=(
        'URL used to support detail of the entry'),)  # Website or URL of the location defined.
    is_internal = models.BooleanField(
        default=False, help_text=('Designates whether the URL is internal to the company'),)  # If true, the URL is only accessable to company users.

    # RLB Processing
    date_scanned = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the URL was last scanned'),)  # Date the URL was last scanned by RLB processing.  Timestamp will be used to randomly test availability.
    is_public = models.BooleanField(
        default=False, help_text=('Designates whether the URL is publically accessible'),)  # RLB processing has found the URL is publically accessible.
    has_page_error = models.BooleanField(
        default=False, help_text=('Designates whether the URL recieves a page error'),)  # If is_public_domain is True after scan then has_page_error will be tested.  If has_page_error is True, then manual review is needed and alert will be sent to entry owner.
    is_recommended = models.BooleanField(
        default=False, help_text=('Designates whether the URL is recommended by RLB'),)  # URL has been reviewed by RLB and is recommend for this type of entry.
    recommended_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='user_recommended', help_text=(
        'User that recommended the URL'),)  # User that recommended the URL
    recommended_notes = models.TextField(
        blank=True, null=True, help_text=('Notes on why the url was recommended reading for other RLB users'),)  # Recommendation notes associated with the URL

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Entry URL")

    def __str__(self):
        """String."""
        return self.name


class RiskType(DefaultFieldsCategory):
    """Risk Type.   The type of business risk associated to the threat scenerio"""

    context = models.TextField(
        blank=True, help_text=('Information on how the entry is associated to the risk type'),)  # Context to better understand why the risk type is tied to the entry

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Risk Types")

    def __str__(self):
        """String."""
        return self.name


class MitigationAdequacy(DefaultFieldsCategory):
    """Mitigation Adequacy.  This best defines the mitigation state."""

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Mitigation Adequacy")

    def __str__(self):
        """String."""
        return self.name
