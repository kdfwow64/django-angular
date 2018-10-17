"""Actor & related models."""
from django.db import models


class Actor(models.Model):
    """Actor.  Used to define and categorize common Threat Actors.  Accounts can add their own threat actors if needed."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the threat actor'),)  # Name of the threat actor.
    description = models.TextField(
        blank=False, help_text=('Description of the actor'),)  # Description of the threat actor
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct actor name'),)  # Used during searches to make sure that you are not duplicating actors.
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this threat actor should be treated as active'),)  # Determines if the threat actor is active
    is_human = models.BooleanField(default=True, help_text=(
        'Designates whether this threat actor is a human'),)  # Determines if the threat actor is a human
    is_internal = models.BooleanField(default=False, help_text=(
        'Designates whether this threat actor internal to the company'),)  # Determines if the threat actor is internal to the company.
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
    account = models.ForeignKey('Account', on_delete=models.PROTECT, default=1, blank=False, related_name='account_actor', help_text=(
        'The account the actor was created under'),)  # By default all threat actors will belong to CORE and be viewable to all companies.  Companies that add actors will only be available to the account the company belongs.  When added to the account, the actor will be available to all companies of the account. Only Account Admin can add intentions.  If Actors are approved by CORE the will be available to all accounts.
    available_intentions = models.ManyToManyField("ActorIntent", through='ThreatActorIntent',
                                                  through_fields=('id_actor', 'id_actorintent'), related_name='ThreatActorIntentions', help_text=('Common intentions of the Threat Actor'),)  # This will be used for reporting and insight content.  It will tie the threat actor to what they intend to do with the asset.
    available_motives = models.ManyToManyField("ActorMotive", through='ThreatActorMotive',
                                               through_fields=('id_actor', 'id_actormotive'), related_name='ThreatActorMotive', help_text=('Common motives of the Threat Actor'),)  # This will be used for reporting and insight content.  It will tie the threat actor to reason they want the asset.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Actors")


class ActorIntent(models.Model):
    """Actor Input.  What intent might the threat Actor have on the Asset"""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the theat actors intent'),)  # Name of the malicious intent the threat Actor may have on the asset.
    description = models.TextField(
        blank=False, help_text=('Description of the threat actors intent'),)  # Name of the description
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed'),)  # This is used to determine the
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Keywords are used find the right category when trying to identify the intent.  Accounts may create their own Intent if not already available.  The goal is to correlate the intent across all accounts for insights.
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this intent should be treated as active'),)  # Determines if the intent is active
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
    account = models.ForeignKey('Account', on_delete=models.PROTECT, default=1, blank=False, related_name='account_intent', help_text=(
        'The account the intention was created under'),)  # By default all intentions will belong to CORE and be viewable to all companies.  Companies that add intentions will only be available to the account the company belongs.  When added to the account, the intention will be available to all companies the account. Only Account Admin can add intentions.  If Intentions are approved by CORE the will be available to all accounts.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Actor Intentions")


class ThreatActorIntent(models.Model):
    ''' This table is used to tie threat actors to their intent.  '''
    id_actor = models.ForeignKey(
        Actor, on_delete=models.PROTECT,)  # Actor Id from the Actor table
    # ActorIntent Id from the ActorIntent table
    id_actorintent = models.ForeignKey(ActorIntent, on_delete=models.PROTECT,)
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the threat actor intent is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False companies will not be able to use the intent for the threat actor.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Date the intent was tied to the threat actor'),)  # Not in use
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='UserCreatedThreatActorIntent', help_text=(
        'User id of the user that created the access'),)
    date_revoked = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the intent tied to the threat actor was revoked, if applicable'),)  # Date company intent was revoked.
    revoked_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='UserRevokedThreatActorIntent', help_text=(
        'User id that revoked the intent from the threat actor'),)  # User id of the admin that revoked the intent from the threat actor

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Threat Actor Intentions")


class ActorMotive(models.Model):
    """Actor Motive."""

    name = models.CharField(
        max_length=45, blank=False, help_text=('Name of the theat actors motive'),)  # Name of the threat actor motive.
    description = models.TextField(
        blank=False, help_text=('Description of the threat actors motive'),)  # Description of the threat actor motive
    sort_order = models.IntegerField(
        blank=True, null=True, help_text=('Sort order that should be displayed'),)  # Order used to display the threat actor motives
    keywords = models.TextField(
        blank=True, null=True,  help_text=('Keywords used to idenify proper category or find correct field name'),)  # Used for searching or defining the threat actor
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this motive should be treated as active'),)  # Determines if the motive is active
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
    account = models.ForeignKey('Account', on_delete=models.PROTECT, default=1, blank=False, related_name='account_motive', help_text=(
        'The account the threat actor motive was created under'),)  # By default all intentions will belong to CORE and be viewable to all companies.  Companies that add intentions will only be available to the account the company belongs.  When added to the account, the intention will be available to all companies the account. Only Account Admin can add intentions.  If Intentions are approved by CORE the will be available to all accounts.

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Actor Motives")


class ThreatActorMotive(models.Model):
    ''' This table is used to tie threat actors to their motive.  '''
    id_actor = models.ForeignKey(
        Actor, on_delete=models.PROTECT)  # ActorId from the Actor table
    # ActorMotive Id from the ActorMotive table
    id_actormotive = models.ForeignKey(ActorMotive, on_delete=models.PROTECT)
    is_active = models.BooleanField(
        default=True, help_text=('Designates whether the threat actor motive is active'),)  # Relationships will never be deleted for auditing purposes.  If is_active is set to False companies will not be able to use the motive for the threat actor.
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, help_text=('Date the motive was tied to the threat actor'),)  # Date the motive was created
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='UserCreatedThreatActorMotive', help_text=(
        'User id of the user that created the threat actor motive'),)
    date_revoked = models.DateTimeField(
        null=True, blank=True, help_text=('Timestamp the motive tied to the threat actor was revoked, if applicable'),)  # Date threat actor motive was revoked.
    revoked_by = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='UserRevokedThreatActorMotive', help_text=(
        'User id that revoked the motive from the threat actor'),)  # User id of the admin that revoked the motive from the threat actor

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Threat Actor Motives")
