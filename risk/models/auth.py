"""User & related models."""
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from risk.lib.user_manager import EmailUserManager
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
)


class User(AbstractBaseUser, PermissionsMixin):
    """User.  Users may belong to multiple accounts and are uniquely identifed by their email address.  Users are tied to accounts with the m2m member field in the Account table and made available to account admin to tie them to specific companies with speicific grants via the m2m user_access field on the company table.  If users are active on an account and not tied to a specific company, they will have access to all companies of the account with the account_type defined in the Account table.  Logic in the application user administration will account for users being added and removed from companies and/or accounts. """

    email = models.EmailField(
        max_length=255, blank=False, unique=True, help_text=('Email address for user. This is the unique identifer of the user'),)  # Email address should be unique at the account level.  However the same email could be present in different accounts.  Note: A user record should not be recreated if the email address already exists.  The existing record should be used.  If the user was previously disabled, the submission should activate the user under the new account only.
    full_name = models.CharField(
        max_length=60, blank=False, help_text=('Full name'),)  # Users full name.  We will use regex to split the lastname from theh full name.  We chose this to support users that do not have a convential first and last name
    last_login = models.DateTimeField(
        null=True, blank=True, help_text=('The last time the user logged into the system'),)  # Date the user last logged into the system.
    date_joined = models.DateTimeField(
        null=True, blank=True, help_text=('Date that the user first logged into the system'),)  # Date the user first logged into the system.  This may be the form date for initial user, but most users will be created by the account owner and will login at a later time.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=('Date that the user was created'),)  # Date the user account was created.  This may be the form date for initial user, but most users will be created by the account owner.
    date_deleted = models.DateTimeField(
        null=True, blank=True, help_text=('Date the user was deleted, if applicable'),)  # Date the user was deleted.  Technincally, no users are deleted, just removed from the contributors view.  If an admin tries to re-add the user it will undeleted the user account and bring it back into view.
    # is_active, is_superuser & is_staff are required for Django
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='created_user', help_text=(
        'User id if created by another user'),)  # User id of the admin that created the user account
    deleted_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='deleted_user', help_text=(
        'User id if deleted by another user'),)  # User id of the admin that deleted the user account
    is_staff = models.BooleanField(
        _('staff'), default=False, help_text=('Designates whether the user can log into this site.'),)
    is_superuser = models.BooleanField(
        _('super'), default=False, help_text=('Designates whether the user is superuser to this site.'),)
    is_active = models.BooleanField(
        _('active'), default=False, help_text=(
            'Designates whether this user should be treated as active'),)  # Need to build email validation to activate account.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = EmailUserManager()

    """The user model functions."""

    def __str__(self):
        """String representation."""
        return self.email

    def get_profile(self):
        """Return user profile."""
        return self.userprofile

    def get_full_name(self):
        """Get full name."""
        return self.full_name

    def get_company_name(self):
        """Get company name."""
        try:
            return self.userprofile.current_company.name
        except:
            return self.userprofile.default_company.name

    def get_company_id(self):
        """Get company id."""
        return self.userprofile.default_company.id

    def get_short_name(self):
        """Get short name."""
        if self.full_name:
            return self.full_name
        else:
            return self.email

    def get_current_company(self):
        """Get current company."""
        return self.userprofile.current_company or self.userprofile.default_company

    def get_last_login(self):
        """Get the last time a the user logged into the system"""
        return self.last_login


class UserProfile(models.Model):
    """
    User profilfe detail to keep the user table clean.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,)
    title = models.CharField(
        max_length=60, blank=True, null=True, help_text=('Title'),)  # Title should be optional for all users
    bio = models.TextField(
        blank=True, null=True, help_text=_('Brief description about career and experience'),)  # Users can submit a brief description of their role.  This will be valuable when using the community.  Optional to all users.
    phone = models.CharField(
        max_length=30, null=True, blank=True, help_text=('Phone number.'),)  # Phone number should be optional.  Global phone numbers formats should be taken into consideration when capturing and displaying the data.
    phone_ext = models.CharField(
        max_length=30, null=True, blank=True, help_text=('Phone extention'),)  # Phone extenstion should be optional and be upto 7 integers in the form.
    country_code = models.CharField(
        max_length=5, null=True, blank=True, help_text=('Country code of user'),)  # Use of 2 character country codes should be leveraged during capture.  May need to get a database of CC as a dropdown for the contributor.
    providence_code = models.CharField(
        max_length=30, null=True, blank=True, help_text=('Select state or providence'),)  # Used for state or providence of the users location.
    use_helpmenu = models.BooleanField(
        default=True, help_text=('Enable help menu functionality'),)  # Should default to true and should be managed in the users profile.  This dictates the use of help and context while using the platform.
    email_subscriber = models.BooleanField(
        default=True, help_text=('Subscribes to the latest risk trends.'),)  # Set to true and should be managed in the users profile.  This setting will be used to send advertising, best practice, and news updates to the contributor.
    utility_field = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Backoffice field used for queries and reporting'),)  # This is for backoffice use.  It will be populated when testing new features or building reports.
    bkof_notes = models.TextField(
        blank=True, null=True, help_text=('Backoffice notes on the user'),)  # Primary notes fot he backoffice regarding the user.  This is different than feedback and other tracked user detail.
    profile_image = models.ImageField(
        null=True, blank=True, help_text=('The profile image and location for the user'),)  # Image for the user profile.  It should default to the generic avatar until the user uploads their own
    due_date_reminder = models.IntegerField(
        default=4, help_text=('Number of days to be reminded when items are due.'),)  # If 0 then no reminder is sent, otherwise this states the number of days to remind a user something is due.
    email_code_reg = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Code generated for email registration.'),)  # Unique code generated for email when the user is created by the admin.
    email_code_date = models.DateTimeField(
        default=timezone.now, null=True, help_text=('Timestamp the email reg code was sent'),)  # Date timestamp the code was generated.  The user will a limited time to leverage the email link to activate thier user account.
    is_verified = models.BooleanField(default=False, help_text=(
        'Designates whether this user has been verified by backoffice'),)  # The user has been verified by the backoffice based on critieria
    is_reputable = models.BooleanField(default=False, help_text=(
        'Designates whether this user has been defined as reputable by backoffice'),)  # The user is been deemed reputable for metrics
    default_company = models.ForeignKey('Company', on_delete=models.PROTECT, blank=True, null=True, related_name='default_company_register', help_text=(
        'The default Company register that is shown first in the user portal'),)  # This is the default company that is opened in the users dashboard.  It can be modified in the user profile.
    current_company = models.ForeignKey('Company', on_delete=models.PROTECT, blank=True, null=True, related_name='current_company_register', help_text=(
        'The current Company register that is shown first in the user portal and user is viewing'),)  # This is the current company that is currently viewed in the users dashboard.  It can be modified in the user profile.

    class Meta:
        """Meta class."""
        verbose_name_plural = ("User Profiles")

    def __str__(self):
        """String representation."""
        return str(self.user.email)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except:
            pass
post_save.connect(post_save_user_model_receiver,
                  sender=settings.AUTH_USER_MODEL)


class AccountType(DefaultFieldsCategory):
    """
    All accounts must be of a certain type for management and billing if applicable.  This ties the account type to the correct level of features
    they consumer has purchased.  Account types will range based on the account needs.
    """

    annual_cost = models.DecimalField(
        default=0, help_text=('Annual cost for the account type'), decimal_places=2, max_digits=30)  # Annual cost in USD for the account type.  This will need to be paid in full before use unless the account is demo/pilot.
    max_user = models.IntegerField(
        default=0, help_text=('Max number of users that can be specified for the account type'),)  # The number of user that can be tied to the account.  Count is taken from AccountMembership model.
    max_company = models.IntegerField(
        default=0, help_text=('Max number of companies that can be specified for the account type'),)  # Number of companys that can be associated with the account.  Count is taken from Company model
    max_company_locations = models.IntegerField(
        default=0, help_text=('Max number of locations per company that can be specified for the account type '),)  # Number of locations that can be used per account.  Locations are company specific.
    max_company_asset = models.IntegerField(
        default=0, help_text=('Max number of assets per company that can be specified for the account type '),)  # Number of assets that can be defined in the account.  Assets are company specific.
    max_company_control = models.IntegerField(
        default=0, help_text=('Max number of controls per company that can be specified for the account type '),)  # Number of controls that can be leveraged for the account.
    max_company_resources = models.IntegerField(
        default=0, help_text=('Max number of resources per company that can be specified for the account type'),)  # Number of resources that can be used for the account type.
    max_register_entries = models.IntegerField(
        default=0, help_text=('Max number of entries per company that can be specified for the account type '),)  # Number of entries that can be used per company
    # Foreign Keys and Relationships

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Account Types")
        ordering = ['sort_order']

    def __str__(self):
        """String representation."""
        return self.name


class Account(DefaultFields):
    """Accounts created by a validated user .  This ties company's and user's together."""

    name = models.CharField(
        max_length=128, blank=True, null=True, help_text=_('Name of the account'),)  # The name of the account will default to NULL, but should take the name of the first company once created.  Account admin should be able to change the name if desired.
    billing_toggle = models.BooleanField(default=True, help_text=(
        'Is the billing contact the same as the account owner'),)  # If billing account is differnt then other data is needed for renewal reminders.
    billing_poc = models.CharField(
        max_length=128, blank=True, null=True, help_text=('Accounts payable billing point of contact name'),)  # Name of the billing contact.  If different from the account owner.  Required
    billing_phone = models.CharField(
        max_length=30, blank=True, null=True, help_text=('Accounts payable phone number'),)  # Phone number of the billing contact.  Optional
    billing_email = models.EmailField(
        max_length=128, blank=True, null=True, help_text=('Accounts payable email'),)  # Email of the billing contact. Required
    renewal_reminder = models.IntegerField(
        default=30, help_text=('Number of days to notify before renewal is due'),)  # Set renewal reminder at 30 days.  This option will not be visible to customers and should be modified by backoffice if needed.  Lever this variable for renewal playbooks.
    tta_user = models.IntegerField(
        default=1440, help_text=('Number of minutes to accept user invitation'),)  # Time To Accept - Number of minutes a user has to accept an invitation.  Default is 24hrs. or 1 day.
    bkof_notes = models.TextField(
        blank=True, null=True, help_text=('Backoffice notes on the account'),)  # Notes on the account by the backoffice
    renewal_ext = models.IntegerField(
        blank=True, default=1, help_text=('Number of months an account is allowed to be extented past renewal'),)  # This option will not be visible to customers and should be modified by backoffice if needed.  Once past renewal_ext value the account will be disabled until payment has been made.
    strong_auth = models.BooleanField(
        default=False, help_text=('Multi-factor authencation requirement is being used'),)  # Need to provide the option to leverage token authenication in conjuction with passwords to meet compliance requirements on the customers side.  This will be a future capability.
    """Application Input"""
    is_reputable = models.BooleanField(default=False, help_text=(
        'Designates whether this account has been defined as reputable by backoffice'),)  # Backoffice has determined that the account is reputable and can be used for reporting and metrics of the platform.
    date_last_paid = models.DateTimeField(
        blank=True, null=True, help_text=('Last the account was paid'),)  # Most recent time of payment.  This will tie to the payment system for detail
    billing_confirmation_code = models.IntegerField(
        blank=True, default=0, help_text=('Conformation code of the last payment'),)  # Conformation code used to provide the billing poc with payment acknowledgement
    # Forgien Keys and Relationships
    account_type = models.ForeignKey('AccountType', on_delete=models.PROTECT, related_name='type_of_account', help_text=(
        'The type of account.for billing and levels of functionality'))  # Type of account being setup.  Should default to the demo verison.  Users can select the level that best supports their needs or can upgrade at a later date to get more functionality.
    authentication_type = models.ForeignKey('AuthenticationType', on_delete=models.PROTECT, default=1, related_name='default_acccount_authenication', help_text=(
        'The type of authentication used for account users'))  # This will be the default user authentication type.  It will default to "1" - PASSWORD, but can be changed on the account adminstration.  When AccountMemberships are created they will default to that authentication type specified in the account, but can be changed as needed on the AccountMembership record.
    owned_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='account_owner', help_text=(
        'User id if deactivated by another user'),)  # User that owns the acccount.  By default this will be the user that performs the inital submission, however may change. (new role in company, deligation needs, etc.)
    member = models.ManyToManyField('User', through='AccountMembership',
                                    through_fields=('id_account', 'id_user'), related_name='AccountMemeberships', help_text=('Users with relationships on the Account'),)  # Users may belong to multiple Accounts.  Users added that have existing registration should be send an email link to join the Account.  New users will need to be created.

    class Meta:
        """Meta Class."""

#    def get_members(self):
#        return "\n".join([m.members for m in self.member.all()])

    def __str__(self):
        """String representation."""
        return self.name


class AccountMembership(DefaultFields):
    # User from the user table
    id_user = models.ForeignKey('User', on_delete=models.PROTECT)
    # Account from the account table
    id_account = models.ForeignKey('Account', on_delete=models.PROTECT)
    date_invited = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, help_text=(
            'Date that the user was invited to join the account'),)  # DateTime the relationship was requested
    invited_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='invited_by_user', help_text=(
        'User id of the user that sent the invitation'),)  # User id of the admin invited the user to the account
    invite_code = models.CharField(max_length=10, blank=True, null=True, help_text=(
        'Random code created for user to match we accepting the invite'),)  # This code will need to match in the user form for the invite to be accepted.  The code will not be transmitted in the email link.  It should be provided verbally or thourgh a separate means to support a two-factor validation.
    date_accepted = models.DateTimeField(
        null=True, blank=True, help_text=(
            'Date that the user accepted the invitation'),)  # DateTime the user accepted the request.
    date_attestation = models.DateField(
        null=True, blank=True, help_text=(
            'Date of the next attestation time for the user'),)  # DateTime the user is required to have attestation perform.  This should be based on the account attestation settings.
    date_temp = models.DateTimeField(
        null=True, blank=True, help_text=(
            'Temp access to the account'),)  # This allows users to be have temperoray access to the account.  If the temp date is set and past the current date, the user should not have access to the account
    invite_reason = models.CharField(max_length=64, help_text=(
        'Optional reason for adding user'))  # Optional reason for adding access.  Should be required if date_temp is set.
    is_admin = models.BooleanField(
        default=False, help_text=('Designates whether the user is an administrator for the account'),)  # If True, the user has full adminstrative access to the account and any companies related to the account.  This setting will dim out any company_role options and automatically create the user into new companies as an administrator.
    is_company_viewable = models.BooleanField(
        default=False, help_text=('Designates whether the user is viewable to all companys related to the account'),)  # Even if set to False only account admin will see the user under the account and will need to add permissions for each company.  If True, company admin will see the account and be able to add the user to company.
    date_revoked = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the user was revoked, if applicable'),)  # Date the user was revoked.  This function will allow an account or company admin to temp or perm disable a user.  Disabled user will still be viewable in case the need to be re-enabled.
    contact_type = models.ForeignKey('ContactType', on_delete=models.PROTECT, default=1, related_name='user_contact_type', help_text=(
        'The type of contact the user will have as default'))  # When the user assigned permissions at the company level, this is the default type that wil be used.  Depending on the company, the user may have a different type in the CompanyContact table.
    authentication_type = models.ForeignKey('AuthenticationType', on_delete=models.PROTECT, blank=True, null=True, related_name='user_acccount_authentication', help_text=(
        'The type of authentication used for account login'))  # This should default to the Account.authentication_type specified in the acocunt table, however can be changed based on the needs of the account for authenincating specific users.  IE Contractors, Auditors, etc
    revoked_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='revoked_user', help_text=(
        'User id if revoked by another user'),)  # User id of the admin that revoked the user account
    date_reactivated = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the user was reactivated, if applicable'),)  # Date the user was deactivated.  This function will allow an account or company admin to temp or perm disable a user.  Disabled user will still be viewable in case the need to be re-enabled.
    reactivated_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='reactivated_user', help_text=(
        'User id if reactivated by another user'),)  # User id of the admin that deactivated the user account
    company_role = models.ForeignKey('UserRole', on_delete=models.PROTECT, default=4, blank=True, null=True, related_name='companyuserrole', help_text=(
        'The default role to be used to setup company user grants for the user'),)  # This will be used to setup the intial grants that a user should have for companies belonging to the account.  Default is set to least priviledge "Auditor"

# Needs to be review for useage.


class UserAccess(DefaultFields):
    """Application Input."""

    # Foreign Keys and Relationships
    user = models.ForeignKey('User', on_delete=models.PROTECT, related_name='useracces', help_text=(
        'User id of the user'),)
    userrole = models.ForeignKey('UserRole', on_delete=models.PROTECT, related_name='useracces', help_text=(
        'User role of the user'),)
    company = models.ForeignKey('Company', on_delete=models.PROTECT, null=True, related_name='useracces', help_text=(
        'Company id if specified'),)
    account = models.ForeignKey('Account', on_delete=models.PROTECT, null=True, related_name='useracces', help_text=(
        'Company id if specified'),)

    def __str__(self):
        """String representation."""
        return self.userrole

    class Meta:
        """Meta class."""
        verbose_name_plural = ("User Access")

'''
class UserLevel(models.Model):
    """This relates to the level access the user is assigned as related to the application (App Admin, Staff, Account etc)."""

    name = models.CharField(
        max_length=30, blank=False, help_text=('Name of the user level'),)  # Not in use
    description = models.TextField(
        blank=False, help_text=('Description of the user level'),)  # Not in use
    # Foreign Keys and Relationships

    def __str__(self):
        """String representation."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("User Levels")
'''


class UserRole(DefaultFieldsCompany):
    """This relates to the role the user will have within the application (View, Contribute, Adminster.)."""

    grants = models.ManyToManyField("UserGrant", through='DefaultRoleGrant',
                                    through_fields=('id_userrole', 'id_usergrant'), related_name='RoleGrants', help_text=('Default grants for a specific role'),)  # Roles are evaluated at both the account and company level.  This mappings specifies the default grants that the role will have for both cases.  Administrators will be able to modify the grants at the company level if needed.
    # Foreign Keys and Relationships

    def __str__(self):
        """String representation."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("User Roles")


class UserGrant(DefaultFieldsCompany):
    """Grant."""

    # Foreign Key and Relationships

    def __str__(self):
        """String representation."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("User Grants")


class DefaultRoleGrant(DefaultFields):
    """ This table is used to set default grants for the user role selected."""
    id_userrole = models.ForeignKey(
        'UserRole', on_delete=models.PROTECT)  # User roles that can be set at the account or company level.
    # Default grants that are associated with the role.  This will be able to
    # be modified during submission, however are used to provide an inital set
    # of grants.
    id_usergrant = models.ForeignKey('UserGrant', on_delete=models.PROTECT)


class RoleTracking(models.Model):
    """Role Tracking."""

    modifed_date = models.DateTimeField(
        auto_now=True, null=True, help_text=('Timestamp the role was created or modifed'),)  # Not in use
    # Not in use
    user_role_from = models.IntegerField(default=0, blank=False, help_text=_(
        'The type of role the user had before being modifed'),)
    # Not in use
    user_role_to = models.IntegerField(blank=False, help_text=_(
        'The role that was added or subtracted for the user'),)
    # Foreign Keys and Relationships
    company = models.ForeignKey('Company', on_delete=models.PROTECT, null=True, related_name='roletracking', help_text=(
        'Company the role modification took place'),)
    modified_by = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='modified_roletracking', help_text=(
        'User id of the user that made the modification'),)
    user = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name='roletracking', help_text=(
        'User id of the user that was modified'),)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Role Tracking")


class AuthenticationType(models.Model):
    """AuthenicationType."""

    name = models.CharField(
        max_length=30, blank=False, help_text=('Name of the authentication type to be used during login'),)  # Users will have multiple methods of authentication based on the security requirements needed.
    description = models.TextField(
        blank=False, help_text=('Description of the authentication type'),)  # Description of the authentication type
    # Foreign Key and Relationships

    def __str__(self):
        """String representation."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Authentication Types")
