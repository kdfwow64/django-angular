# This file is used as a template for various model formats in efforts to
# keep common terminology and layouts organized.

    lowercaseclassname = models.ForeignKey(
        classname, null=True, related_name='somename_related', help_text=('Date that the asset type was created'),)

    class Meta:
        """Meta class."""

        ordering = ['name', -'name2']
        unique_together = ['firststring', 'secondstring']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
            models.Index(fields=['last_name'], name='last_name_idx'), ]
        verbose_name = "pizza"
        order_with_respect_to = 'question'
        get_latest_by = "order_date"

    def __str__(self):
        """String."""
        return self.name

    string - blank = False, blank = True
    int - default = 0 blank = True
    import pytz
    date = models.DateTimeField(null=True, blank=True)
    # Not in use
    date = = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text=('Click'),)
    boolean default = True
    user DecimalField for money

Default Class Model


class Default(models.Model):
    """Form Input"""
    """Application Input"""
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this field row should be treated as active'),)  # Not in use
    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the '),)  # Not in use
    desc = models.TextField(
        blank=False, help_text=('Description of the asset'),)  # Not in use
    abbrv = models.CharField(
        max_length=30, blank=True, help_text=('Abbreviation of the name'),)  # Not in use
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed'),)  # Not in use
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the individual was created'),)  # Not in use
    date_modified = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,  help_text=('Timestamp the individual was created'),)  # Not in use
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the individual was deactivated'),)  # Not in use
    date_deleted = models.DateTimeField(
        null=True, blank=True,  help_text=('Timestamp the individual was created'),)  # Not in use
    # Foreign Key and Relationships
    info = models.ForeignKey('Info', null=True, related_name='default', help_text=(
        'Information detail for the field '),)
    keywords = models.ForeignKey('Keywords', null=True, related_name='default', help_text=(
        'Keywords to help find the object '),)
    owner = models.ForeignKey('CompanyContact', null=True, related_name='default', help_text=(
        ' Who owns the task'),)
    created_by = models.ForeignKey('User', null=True, related_name='created_default', help_text=(
        'User id of the user that created the field'),)
    modified_by = models.ForeignKey('User', null=True, related_name='modified_default', help_text=(
        'User id that last modified the field'),)
    deactivated_by = models.ForeignKey('User', null=True, related_name='deactivated_default', help_text=(
        'User id if deactivated by another user'),)
    deleted_by = models.ForeignKey('User', null=True, related_name='deleted_default', help_text=(
        'User id if deleted by another user'),)

    class Meta:
        """Meta class."""
        ordering = ['name', -'name2']
        unique_together = ['firststring', 'secondstring']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
            models.Index(fields=['last_name'], name='last_name_idx'), ]
        verbose_name = "pizza"
        order_with_respect_to = 'question'
        get_latest_by = "order_date"

    def __str__(self):
        """String."""
        return self.name


--------------------------------------------------------------------------------------------

    is_verified = models.BooleanField(default=False, help_text=(
        'Designates whether this <Insert> has been verified by backoffice'),)
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this <Insert> is currently active'),)
    is_reputable = models.BooleanField(default=False, help_text=(
        'Designates whether this <Insert> has been defined as reputable by backoffice'),)

    'is_active',
    'is_verified',
    'is_reputable',

    reputable_ < ClassName > = < ClassName > ReputableManager()
    active_ < ClassName > = < ClassName > ActiveManager()


class < ClassName > ActiveManager(models.Manager):
    # Find active <classname> objects for queries and filters

    def get_queryset(self):
        return super( < ClassName > ActiveManager, self).get_queryset().filter(is_active=True)


class < ClassName > VerifiedManager(models.Manager):
    # Find verified <classname> objects for queries and filters

    def get_queryset(self):
        return super( < ClassName > VerifiedManager, self).get_queryset().filter(is_verified=True)


class < ClassName > ReputableManager(models.Manager):
    # Find reputable <classname> objects for queries and filters

    def get_queryset(self):
        return super( < ClassName > ReputableManager, self).get_queryset().filter(is_reputable=True)


#  ManyToManyField - Through  models.py


member = models.ManyToManyField('User', through='AccountMembership',
                                through_fields=('Account', 'user'), related_name='AccountMemeberships', help_text=('Users with relationships on the Account'),)  # Users may belong to multiple Accounts.  Users added that have existing registration should be send an email link to join the Account.  New users will need to be created.


class AccountMembership(models.Model):
    user = models.ForeignKey(User)  # User from the user table
    account = models.ForeignKey(Account)  # Account from the account table
    date_requested = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=(
            'Date that the user was created'),)  # DateTime the relationship was requested
    date_joined = models.DateTimeField(
        null=True, blank=True, help_text=(
            'Date that the user joined the account'),)  # DateTime the user accepted the request.
    date_attestation = models.DateField(
        null=True, blank=True, help_text=(
            'Date of the next attestation time for the user'),)  # DateTime the user is required to have attestation perform.  This should be based on the account attestation settings.
    date_temp = models.DateTimeField(
        null=True, blank=True, help_text=(
            'Temp access to the account'),)  # This allows users to be have temperoray access to the account.  If the temp date is set and past the current date, the user should not have access to the account
    invite_reason = models.CharField(max_length=64, help_text=(
        'Optional reason for adding user'))  # Optional reason for adding access.  Should be required if date_temp is set.
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the user / account relationship is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False the user will not have access to the account.
    date_deactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the user was deactivated, if applicable'),)  # Date the user was deactivated.  This function will allow an account or company admin to temp or perm disable a user.  Disabled user will still be viewable in case the need to be re-enabled.
    deactivated_by = models.ForeignKey('User', blank=True, null=True, related_name='deactivated_user', help_text=(
        'User id if deactivated by another user'),)  # User id of the admin that deactivated the user account
    date_reactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the user was reactivated, if applicable'),)  # Date the user was deactivated.  This function will allow an account or company admin to temp or perm disable a user.  Disabled user will still be viewable in case the need to be re-enabled.
    reactivated_by = models.ForeignKey('User', blank=True, null=True, related_name='reactivated_user', help_text=(
        'User id if reactivated by another user'),)  # User id of the admin that deactivated the user account
    user_role = models.ForeignKey('UserRole', blank=True, null=True, related_name='userrole', help_text=(
        'Role of the user'),)


#  ManyToManyField - Through  admin.py

class AccountMembershipInline(admin.TabularInline):

    model = AccountMembership
    extra = 1
