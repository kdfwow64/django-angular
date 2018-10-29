"""Utils."""
from django.db import models
from django.utils import timezone


class Selector(models.Model):
    """Used to better understand Boolean variables"""
    YES = 'Y'
    NO = 'N'
    RED = 'R'
    AMBER = 'A'
    GREEN = 'G'
    UNKNOWN = 'U'
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PERCENT = 'P'
    FIXED = 'F'
    TIMED = 'T'
    YES_NO = (('Y', 'Yes'), ('N', 'No'))
    RAG = (('R', 'Red'), ('A', 'Amber'), ('G', 'Green'), ('U', 'Unknown'))
    HML = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('U', 'Unknown'))
    EF = (('P', 'Percentage of Asset Value'), ('F', 'Fixed Impact Value'))
    ASSET = (('F', 'Fixed Value'), ('P', 'Percent of Revenue'),
             ('T', 'Time Based Value'))
    LOSS = (('F', 'Fixed Value'), ('P', 'Percent of Revenue'))


class DefaultFields(models.Model):
    """Default fields used for most models."""

    # is_active determines if the field is available for use by the
    # application.  is_active fields set to false should not be avaliable for
    # use by the contributor.
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this field row should be treated as an active field and availiable for use by the application'),)
    # is_deleted determines if the field has been deleted.  All inputs into
    # the application should be retained for continuity and evidence.  If
    # is_deleted is set to True, if must be approved by an application admin
    # before change back to False.
    is_deleted = models.BooleanField(default=False, help_text=(
        'Designates whether this field row has been deleted'),)
    # Created when field is initallly created in the application.
    date_created = models.DateTimeField(
        editable=False, help_text=('Timestamp the field was created'),)
    date_modified = models.DateTimeField(null=True, blank=True, help_text=(
        'Timestamp the field was last modified'),)  # Modified when the field was last modified in the application.
    date_deactivated = models.DateTimeField(null=True, blank=True, help_text=(
        'Timestamp the field was last deactivated'),)  # This defines when the field was last deactivated.
    date_deleted = models.DateTimeField(null=True, blank=True,  help_text=(
        'Timestamp the individual was created'),)  # Not in use
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, default=13, related_name='%(app_label)s_%(class)s_related_created', help_text=(
        'User id of the user that created the field'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, default=13, related_name='%(app_label)s_%(class)s_related_modified', help_text=(
        'User id that last modified the field'),)
    deactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='%(app_label)s_%(class)s_related_deactivated', help_text=(
        'User id that last deactivated the field'),)
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, related_name='%(app_label)s_%(class)s_related_deleted', help_text=(
        'User id that last deleted the field'),)

    class Meta:
        """Meta class."""
        indexes = [
            models.Index(fields=['date_modified']),
        ]
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(DefaultFields, self).save(*args, **kwargs)


class DefaultFieldsCompany(DefaultFields):
    """Models that are used for categorizing data"""

    # Name of the field.
    name = models.CharField(max_length=128, blank=True,
                            null=True, help_text=('Name of the field'),)
    description = models.TextField(blank=True, null=True, help_text=(
        'Description of the field'),)  # Description of the field.
    # Foreign Key and Relationships
    company = models.ForeignKey('Company', default=1, on_delete=models.PROTECT, blank=False, related_name='%(app_label)s_%(class)s_related_company', help_text=(
        'Company id for the company that manages the field'),)  # Company that defined the field.

    class Meta:
        """Meta class."""
        indexes = [
            models.Index(fields=['company']),
        ]
        abstract = True


class DefaultFieldsEntry(DefaultFields):
    """Models that are used for categorizing data"""

    # Name of the field.
    name = models.CharField(max_length=225, blank=True,
                            null=True, help_text=('Summary of the %(class)s'),)
    description = models.TextField(blank=True, null=True, help_text=(
        'Description of the field'),)  # Description of the field.
    # Foreign Key and Relationships
    entry = models.ForeignKey('Entry', default=1, on_delete=models.PROTECT, blank=False, related_name='%(app_label)s_%(class)s_related_entry', help_text=(
        'Entry id for the company that manages the field'),)  # Entry that defined the field.

    class Meta:
        """Meta class."""
        indexes = [
            models.Index(fields=['company']),
        ]
        abstract = True


class DefaultFieldsCategory(DefaultFieldsCompany):
    """Models that are used for categorizing data"""

    # Name of the field.
    abbrv = models.CharField(max_length=30, null=True, blank=True, help_text=(
        'Abbreviation of the name'),)  # Abbreviation of the name field.
    sort_order = models.IntegerField(default=0, blank=True, null=True, help_text=(
        'Sort order the field should be in for form selection'),)  # Used for viewing and field choices
    keywords = models.TextField(blank=True, null=True,  help_text=(
        'Keywords used to idenify proper category or find correct field name'),)  # Used to find the correct field
    # Used to help contributors understand the category and how it may apply.
    example1 = models.TextField(blank=True, null=True,  help_text=(
        'Pratcial example of the category'),)
    # Used to help contributors understand the category and how it may apply.
    example2 = models.TextField(blank=True, null=True,  help_text=(
        'Pratcial example of the category'),)

    class Meta:
        """Meta class."""
        abstract = True


class DefaultFieldsEvaluation(DefaultFields):
    """Used for Evaluation Models"""

    notes = models.TextField(blank=True, help_text=(
        'Notes regarding the evaluation'),)  # Updates to the evaluation
    # is_approved determines if the has been approved by a contributor with
    # approval rights.
    is_approved = models.BooleanField(default=False, help_text=(
        'Designates whether the evaluation has been approved'),)
    date_evaluated = models.DateTimeField(null=True, blank=True, help_text=(
        'Timestamp the evaluation ended'),)  # Date the user completed submitted the evaluation
    # Foreign Key and Relationships
    evaluated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='%(app_label)s_%(class)s_related_evaluator', help_text=(
        'The user that performed the evaluation'),)  # User that completed the evaluation.
    approved_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='%(app_label)s_%(class)s_related__approver', help_text=(
        'The user that performed the evaluation'),)  # User that completed the evaluation.

    class Meta:
        """Meta class."""
        indexes = [
            models.Index(fields=['is_approved']),
        ]
        abstract = True
