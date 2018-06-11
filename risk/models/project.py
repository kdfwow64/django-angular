"""Projects & related models."""
from django.db import models


class Project(models.Model):
    """Projects."""

    name = models.CharField(
        max_length=128, blank=False, help_text=('Name of the project'),)  # Name of the project.
    executive_summary = models.TextField(
        blank=False, help_text=('Description of the project'),)  # Description of the project.
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether the project should be treated as active'),)  # Is the project currently active
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Timestamp the project was created'),)  # Date the project was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text=('Timestamp the project was last modified'),)  # Date the project was last modified
    date_start = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the project started'),)  # Time the project was initally scheduled to start
    date_close = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the project closed'),)  # Time the project was initally scheduled to closed.
    was_cancelled = models.BooleanField(default=False, help_text=(
        'Selection if the project was cancelled'),)  # Defines if the project was cancelled
    reason_cancelled = models.TextField(
        blank=True, help_text=('Reason the project was cancelled'),)  # Reason the project was cancelled
    budget_capex = models.DecimalField(blank=True, default=0, max_digits=30, decimal_places=2, help_text=(
        'Inital budget set for the capital expenditure of project'),)
    budget_opex = models.DecimalField(blank=True, default=0, max_digits=30, decimal_places=2, help_text=(
        'Inital budget set for the annual operational expenditure of project'),)
    # Foreign Key and Relationships
    company = models.ForeignKey('Company', on_delete=models.PROTECT, null=True, related_name='project_company', help_text=(
        'Company associated with the project '),)  # Company that the project belongs
    organizer = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='project_organizer', help_text=(
        'Organzier of the project'),)  # User that created the project.
    entries = models.ManyToManyField('Entry', through='ProjectEntryMap',
                                     through_fields=('id_project', 'id_entry'), related_name='ProjectEntryMaps', help_text=('Entries that are associated to the project.'),)  # used to define what entries are associated to the project.
    '''
    project_type = models.ForeignKey('MeetingType', on_delete=models.PROTECT, null=True, related_name='meeting', help_text=(
        'Type of meeting'),)  # The type of meeting


    stakeholders = models.ManyToManyField('CompanyContact', through='MeetingAttendeeMap',
                                       through_fields=('id_meeting', 'id_companycontact'), related_name='MeetingAttedees', help_text=('Company contacts that were invited to the meeting.'),)  # Used to determine what company contacts were invited to the meeting.
    milestones = models.ManyToManyField('MeetingTopic', through='MeetingTopicMap',
                                    through_fields=('id_meeting', 'id_meetingtopic'), related_name='MeetingTopicMaps', help_text=('Topics that are discussed in the meeting.'),)  # used to define what meeting topics are associated to the meeting.  Can also be used to produce an agenda.
    extentions = models.ManyToManyField('MeetingTopic', through='MeetingTopicMap',
                                    through_fields=('id_meeting', 'id_meetingtopic'), related_name='MeetingTopicMaps', help_text=('Topics that are discussed in the meeting.'),)  # used to define what meeting topics are associated to the meeting.  Can also be used to produce an agenda.
    '''

    def __str__(self):
        """String."""
        return self.name


class ProjectEntryMap(models.Model):
    """Project Entries."""

    id_project = models.ForeignKey('Project', on_delete=models.PROTECT, null=True, related_name='projectentry', help_text=(
        'The project associated with the entry'),)
    id_entry = models.ForeignKey('Entry', on_delete=models.PROTECT, null=True, related_name='entryproject', help_text=(
        'Entry that applies to the project'),)

    def __str__(self):
        """String."""
        return self.id_entry

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Project Entries")


class ProjectAssumption(models.Model):
    """Project Assumptions.  Used to define any assumptions made about the project"""
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this assumption should be treated as active'),)  # Determines if the assumption is active
    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the assumption'),)  # Summary of the assumption used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the assumption'),)  # Detail of the assumption if more infromation is warranted
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the assumption was created'),)  # Timestamp the assumption was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the assumption was last modified'),)  # Timestamp the assumption was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the assumption was deactivated'),)  # Timestamp the assumption was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the assumption was created'),)  # Timestamp the assumption was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_assumption', help_text=(
        'User id of the user that created the assumption'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_assumption', help_text=(
        'User id that last modified the assumption'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_assumption', help_text=(
        'User id if deactivated by another user'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_assumption', help_text=(
        'Project the assumption is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Assumptions"

    def __str__(self):
        """String."""
        return self.summary


class ProjectSuccessCriteria(models.Model):
    """Project Success Criteria.  Used to define the success criteria to measurements of the project"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this criteria should be treated as active'),)  # Determines if the success criteria is active
    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the success criteria used to determine effectiveness'),)  # Summary of the success criteria used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the success criteria'),)  # Detail of the success criteria if more infromation is warranted
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the success criteria was created'),)  # Timestamp the success criteria was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the success criteria was last modified'),)  # Timestamp the success criteria was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the success criteria was deactivated'),)  # Timestamp the success criteria was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the success criteria was created'),)  # Timestamp the success criteria was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_successcriteria', help_text=(
        'User id of the user that created the success criteria'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_successcriteria', help_text=(
        'User id that last modified the success criteria'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_successcriteria', help_text=(
        'User id if deactivated by another user'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_successcriteria', help_text=(
        'Project the success criteria is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Success Criteria"

    def __str__(self):
        """String."""
        return self.summary


class ProjectBenefit(models.Model):  # Need to complete
    """Project Benifits.  Used define the business benifits of the project"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this benefit should be treated as active'),)  # Determines if the benefit is active
    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the benefit for the company'),)  # Summary of the benefit used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the benefit'),)  # Detail of the benefit if more infromation is warranted
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the benefit was created'),)  # Timestamp the benifit was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the benefit was last modified'),)  # Timestamp the benifit was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the benefit was deactivated'),)  # Timestamp the benifit was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the benefit was created'),)  # Timestamp the benifit was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_benefit', help_text=(
        'User id of the user that created the benefit'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_benefit', help_text=(
        'User id that last modified the benefit'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_benefit', help_text=(
        'User id if deactivated by another user'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT,  related_name='project_benefit', help_text=(
        'Project the benefit is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Benefits"

    def __str__(self):
        """String."""
        return self.summary


class ProjectMilestone(models.Model):
    """Project Milestones  Used to define major milestones of the project timeline"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this milestone should be treated as active'),)  # Determines if the milestone is active
    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the milestone for the company'),)  # Summary of the milestone used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the milestone'),)  # Detail of the milestone if more infromation is warranted
    date_start = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the milestone was scheduled to start'),)  # Timestamp the milestone was start
    date_complete = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp of the milestone target completition date'),)  # Timestamp the milestone was complete
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the milestone was created'),)  # Timestamp the milestone was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the milestone was last modified'),)  # Timestamp the milestone was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the milestone was deactivated'),)  # Timestamp the milestone fit was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the milestone was created'),)  # Timestamp the milestone was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_milestone', help_text=(
        'User id of the user that created the milestone'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_milestone', help_text=(
        'User id that last modified the milestone'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_milestone', help_text=(
        'User id if deactivated by another user'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_milestone', help_text=(
        'Project the milestone is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Milestones"

    def __str__(self):
        """String."""
        return self.summary


class ProjectRisk(models.Model):
    """Project Risk  Used to define major risk items associated with the project"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this risk should be treated as active'),)  # Determines if the risk is active
    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the risk for the company'),)  # Summary of the risk used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the risk'),)  # Detail of the risk if more infromation is warranted
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the risk was created'),)  # Timestamp the risk was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the risk was last modified'),)  # Timestamp the risk was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the risk was deactivated'),)  # Timestamp the risk fit was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the risk was created'),)  # Timestamp the risk was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_projectrisk', help_text=(
        'User id of the user that created the risk'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_projectrisk', help_text=(
        'User id that last modified the risk'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_projectrisk', help_text=(
        'User id if deactivated by another user'),)
    risk_type = models.ForeignKey('RiskType', on_delete=models.PROTECT, related_name='projectrisk_risktype', help_text=(
        'The risk type associated to the entry'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_projectrisk', help_text=(
        'Project the risk is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Risks"

    def __str__(self):
        """String."""
        return self.summary


class ProjectRiskType(models.Model):
    """Project Risk  Used to define major risk items associated with the project"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this risk should be treated as active'),)  # Determines if the risk type is active
    name = models.CharField(
        max_length=30, blank=False, help_text=('Name of the risk type for the company'),)  # Summary of the risk type used for high level overview
    desc = models.TextField(
        blank=False, help_text=('Additional description of the risk type'),)  # Detail of the risk type if more infromation is warranted
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the risk type was created'),)  # Timestamp the risk type was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the risk type was last modified'),)  # Timestamp the risk type was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the risk type was deactivated'),)  # Timestamp the risk typefit was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the risk type was created'),)  # Timestamp the risk type was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', default=1, on_delete=models.PROTECT, related_name='created_projectrisktype', help_text=(
        'User id of the user that created the risk type'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_projectrisktype', help_text=(
        'User id that last modified the risk type'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_projectrisktype', help_text=(
        'User id if deactivated by another user'),)
    account = models.ForeignKey('Account', on_delete=models.PROTECT, default=1, blank=False, related_name='account_projectrisktype', help_text=(
        'Account that owns the project risk type'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Risk Types"

    def __str__(self):
        """String."""
        return self.name


class ProjectBudgetChange(models.Model):
    """Project Budget Change  Used to define major budget change items associated with the project"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this budget change should be treated as active'),)  # Determines if the budget change is active
    amount = models.DecimalField(blank=True, default=0, max_digits=30, decimal_places=2, help_text=(
        'Inital budget set for the capital expenditure of project'),)
    is_increase = models.BooleanField(default=True, help_text=(
        'Designates whether this budget change should be treated as an increase'),)  # If True, increase to budget - If False, decrease in budget
    is_capex = models.BooleanField(default=True, help_text=(
        'Designates whether this budget change should be applied to capital expenditure'),)  # If true, capital expenditure - If False, operational expenditure
    reason = models.TextField(
        blank=False, help_text=('Additional detail of the budget change'),)  # Detail of the budget change if more infromation is warranted
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the budget change was created'),)  # Timestamp the budget change was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the budget change was last modified'),)  # Timestamp the budget change was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the budget change was deactivated'),)  # Timestamp the budget change fit was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the budget change was created'),)  # Timestamp the budget change was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_budgetchange', help_text=(
        'User id of the user that created the budget change'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_budgetchange', help_text=(
        'User id that last modified the budget change'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_budgetchange', help_text=(
        'User id if deactivated by another user'),)
    risk_type = models.ForeignKey('RiskType', on_delete=models.PROTECT, related_name='risktype_budgetchange', help_text=(
        'The budget change type associated to the reason for the budget change'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_budgetchange', help_text=(
        'Project the budget change is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Budget Changes"

    def __str__(self):
        """String."""
        return self.reason


class ProjectDateChange(models.Model):
    """Project Date Change Used to define date changes in the project"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this date change should be treated as active'),)  # Determines if the date change is active
    day = models.IntegerField(blank=True, default=0, help_text=(
        'Number of days for the change'),)  # Number of days to add or subtract from the project
    # If True, add days to project - If False, subtract days from project
    is_added = models.BooleanField(default=True, help_text=(
        'Designates whether the number of days should be added to the project'),)
    reason = models.TextField(
        blank=False, help_text=('Additional detail of the date change'),)  # Detail of the date change if more infromation is warranted
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the date change was created'),)  # Timestamp the date change was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the date change was last modified'),)  # Timestamp the date change was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the date change was deactivated'),)  # Timestamp the date change fit was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the date change was created'),)  # Timestamp the date change was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_datechange', help_text=(
        'User id of the user that created the date change'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_datechange', help_text=(
        'User id that last modified the date change'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_datechange', help_text=(
        'User id if deactivated by another user'),)
    risk_type = models.ForeignKey('RiskType', on_delete=models.PROTECT, related_name='risktype_datechange', help_text=(
        'The date change type associated to the reason for the date change'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_datechange', help_text=(
        'Project the date change is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Date Changes"

    def __str__(self):
        """String."""
        return self.reason


class ProjectUAT(models.Model):
    """Project User Acceptance Testing  Used to define user acceptance testing procedures if needed"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this UAT should be treated as active'),)  # Determines if the UAT is active
    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the UAT for the company'),)  # Summary of the UAT used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the UAT'),)  # Detail of the UAT if more infromation is warranted
    result = models.CharField(
        max_length=600, blank=False, help_text=('Expected results from the UAT'),)  # Desired results of the UAT used for high level overview
    is_acceptable = models.BooleanField(default=True, help_text=(
        'Designates whether test results from UAT were acceptable'),)  # If True, results passed - If false, results failed
    date_start = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the UAT was scheduled to start'),)  # Timestamp the UAT was start
    date_complete = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp of the UAT target completition date'),)  # Timestamp the UAT was complete
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the UAT was created'),)  # Timestamp the UAT was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the UAT was last modified'),)  # Timestamp the UAT was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the UAT was deactivated'),)  # Timestamp the UAT fit was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the UAT was created'),)  # Timestamp the UAT was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_uat', help_text=(
        'User id of the user that created the UAT'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_uat', help_text=(
        'User id that last modified the UAT'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_uat', help_text=(
        'User id if deactivated by another user'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_uat', help_text=(
        'Project the UAT is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project UAT"

    def __str__(self):
        """String."""
        return self.summary


class ProjectUpdate(models.Model):
    """Project Updates  Used to provide the latest status on a project"""

    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this update should be treated as active'),)  # Determines if the update is active
    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the update for the project'),)  # Summary of the update used for high level overview
    desc = models.TextField(
        blank=False, help_text=('Additional detail of the update'),)  # Detail of the update if more infromation is warranted
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the update was created'),)  # Timestamp the update was created
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True,  help_text=('Timestamp the update was last modified'),)  # Timestamp the update was last modified
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the update was deactivated'),)  # Timestamp the update fit was deactivated
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the update was created'),)  # Timestamp the update was deleted
    # Foreign Key and Relationships
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_projectupdate', help_text=(
        'User id of the user that created the update'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='modified_projectupdate', help_text=(
        'User id that last modified the update'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deactivated_projectupdate', help_text=(
        'User id if deactivated by another user'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_projectupdate', help_text=(
        'Project the update is associated'),)
    indicator = models.ForeignKey('RAGIndicator', on_delete=models.PROTECT, related_name='project_statusindicator', help_text=(
        'Used to determine the visual indicator of the project'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Updates"

    def __str__(self):
        """String."""
        return self.summary
