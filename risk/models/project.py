"""Projects & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
    DefaultFieldsContext,
)


class Project(DefaultFieldsCompany):
    """Projects."""

    date_start = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the project started'),)  # Time the project was initally scheduled to start
    date_close = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the project closed'),)  # Time the project was initally scheduled to closed.
    estimated_days = models.IntegerField(blank=True, default=0, help_text=(
        'Estimated number of days to complete the project.'),)  # This will be used in conjuction with the date_start to determine an estimated completion date.  Any addtion date changes after date_start will be tracked via the ProjectDateChange model.
    was_cancelled = models.BooleanField(default=False, help_text=(
        'Selection if the project was cancelled'),)  # Defines if the project was cancelled
    reason_cancelled = models.TextField(
        blank=True, help_text=('Reason the project was cancelled'),)  # Reason the project was cancelled
    budget_capex = models.DecimalField(blank=True, default=0, max_digits=30, decimal_places=2, help_text=(
        'Inital budget set for the capital expenditure of project'),)
    budget_opex = models.DecimalField(blank=True, default=0, max_digits=30, decimal_places=2, help_text=(
        'Inital budget set for the annual operational expenditure of project'),)
    # Foreign Key and Relationships
    organizer = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='project_organizer', help_text=(
        'Organzier of the project'),)  # User that created the project.
    entries = models.ManyToManyField('Entry', through='ProjectEntry',
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


class ProjectEntry(DefaultFields):
    """Through field for Project.  Project Entries."""

    id_project = models.ForeignKey('Project', on_delete=models.PROTECT, null=True, related_name='projectentry', help_text=(
        'The project associated with the entry'),)
    id_entry = models.ForeignKey('Entry', on_delete=models.PROTECT, null=True, related_name='entryproject', help_text=(
        'Entry that applies to the project'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Project Entries")

    def __str__(self):
        """String."""
        return self.id_entry


class ProjectAssumption(DefaultFields):
    """Project Assumptions.  Used to define any assumptions made about the project"""
    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the assumption'),)  # Summary of the assumption used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the assumption'),)  # Detail of the assumption if more infromation is warranted
    # Foreign Key and Relationships
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_assumption', help_text=(
        'Project the assumption is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Assumptions"

    def __str__(self):
        """String."""
        return self.summary


class ProjectSuccessCriteria(DefaultFields):
    """Project Success Criteria.  Used to define the success criteria to measurements of the project"""

    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the success criteria used to determine effectiveness'),)  # Summary of the success criteria used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the success criteria'),)  # Detail of the success criteria if more infromation is warranted
    # Foreign Key and Relationships
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_successcriteria', help_text=(
        'Project the success criteria is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Success Criteria"

    def __str__(self):
        """String."""
        return self.summary


class ProjectBenefit(DefaultFields):  # Need to complete
    """Project Benifits.  Used define the business benifits of the project"""

    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the benefit for the company'),)  # Summary of the benefit used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the benefit'),)  # Detail of the benefit if more infromation is warranted
    # Foreign Key and Relationships
    project = models.ForeignKey('Project', on_delete=models.PROTECT,  related_name='project_benefit', help_text=(
        'Project the benefit is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Benefits"

    def __str__(self):
        """String."""
        return self.summary


class ProjectMilestone(DefaultFields):
    """Project Milestones  Used to define major milestones of the project timeline"""

    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the milestone for the company'),)  # Summary of the milestone used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the milestone'),)  # Detail of the milestone if more infromation is warranted
    date_start = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the milestone was scheduled to start'),)  # Timestamp the milestone was start
    date_complete = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp of the milestone target completition date'),)  # Timestamp the milestone was complete
    # Foreign Key and Relationships
    rag = models.ForeignKey('RAGIndicator', on_delete=models.PROTECT, default=1, related_name='projectmilestone_rag', help_text=(
        'RAG indicator of the milestone'),)  # Defines the current state of the project.
    completed_by = models.ForeignKey('User', on_delete=models.PROTECT, default=13, related_name='projectmilestone_usercompleted', help_text=(
        'User id of the user that completed the milestone'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_milestone', help_text=(
        'Project the milestone is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Milestones"

    def __str__(self):
        """String."""
        return self.summary


class ProjectProgress(DefaultFields):
    """Project Progress topics used to determine the recent and current actions for milestones"""

    summary = models.TextField(
        blank=False, help_text=('Summary of the topics for the project'),)  # Detail of the milestone if more infromation is warranted
    # Foreign Key and Relationships
    is_enabled = models.BooleanField(default=True, help_text=(
        'Designates whether this progress update should be present in the report'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_progress', help_text=(
        'Project the milestone is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Progress"

    def __str__(self):
        """String."""
        return self.summary


class ProjectNextStep(DefaultFields):
    """Project Next Steps topics used to define the upcoming items in a project"""

    summary = models.TextField(
        blank=False, help_text=('Summary of the next steps for the project'),)  # Detail of the milestone if more infromation is warranted
    # Foreign Key and Relationships
    is_enabled = models.BooleanField(default=True, help_text=(
        'Designates whether this topic should be present in the report'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_nextstep', help_text=(
        'Project the milestone is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Next Steps"

    def __str__(self):
        """String."""
        return self.summary


class ProjectRisk(DefaultFields):
    """Project Risk  Used to define major risk items associated with the project"""

    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the risk for the company'),)  # Summary of the risk used for high level overview
    detail = models.TextField(
        blank=False, help_text=('Additional detail of the risk'),)  # Detail of the risk if more infromation is warranted
    # Foreign Key and Relationships
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


class ProjectRiskType(DefaultFieldsCategory):
    """Project Risk  Used to define major risk items associated with the project"""

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Risk Types"

    def __str__(self):
        """String."""
        return self.name


class ProjectBudgetChange(DefaultFields):
    """Project Budget Change  Used to define major budget change items associated with the project"""

    amount = models.DecimalField(blank=True, default=0, max_digits=30, decimal_places=2, help_text=(
        'Inital budget set for the capital expenditure of project'),)
    is_increase = models.BooleanField(default=True, help_text=(
        'Designates whether this budget change should be treated as an increase'),)  # If True, increase to budget - If False, decrease in budget
    is_capex = models.BooleanField(default=True, help_text=(
        'Designates whether this budget change should be applied to capital expenditure'),)  # If true, capital expenditure - If False, operational expenditure
    reason = models.TextField(
        blank=False, help_text=('Additional detail of the budget change'),)  # Detail of the budget change if more infromation is warranted
    # Foreign Key and Relationships
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


class ProjectDateChange(DefaultFields):
    """Project Date Change Used to define date changes in the project"""

    days = models.IntegerField(blank=True, default=0, help_text=(
        'Number of days for the change'),)  # Number of days to add or subtract from the project
    # If True, add days to project - If False, subtract days from project
    is_added = models.BooleanField(default=True, help_text=(
        'Designates whether the number of days should be added to the project'),)
    reason = models.TextField(
        blank=False, help_text=('Additional detail of the date change'),)  # Detail of the date change if more infromation is warranted
    # Foreign Key and Relationships
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


class ProjectUAT(DefaultFields):
    """Project User Acceptance Testing  Used to define user acceptance testing procedures if needed"""

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
    # Foreign Key and Relationships
    completed_by = models.ForeignKey('User', on_delete=models.PROTECT, default=13, related_name='projectUAT_usercompleted', help_text=(
        'User id of the user that completed the milestone'),)
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_uat', help_text=(
        'Project the UAT is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project UAT"

    def __str__(self):
        """String."""
        return self.summary


class ProjectUpdate(DefaultFields):
    """Project Updates  Used to provide the latest status on a project"""

    summary = models.CharField(
        max_length=600, blank=False, help_text=('Summary of the update for the project'),)  # Summary of the update used for high level overview
    description = models.TextField(
        blank=False, help_text=('Additional detail of the update'),)  # Detail of the update if more infromation is warranted
    rag = models.ForeignKey('RAGIndicator', on_delete=models.PROTECT, default=1, related_name='project_rag', help_text=(
        'RAG indicator of the project'),)  # Defines the current state of the project.
    # Foreign Key and Relationships
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='project_projectupdate', help_text=(
        'Project the update is associated'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = "Project Updates"

    def __str__(self):
        """String."""
        return self.summary
