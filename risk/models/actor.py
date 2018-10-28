"""Actor & related models."""
from django.db import models
from risk.models.utility import (
    Selector,
    DefaultFields,
    DefaultFieldsEntry,
    DefaultFieldsCompany,
    DefaultFieldsCategory,
)


class Actor(DefaultFieldsCategory):
    """Actor.  Used to define and categorize common Threat Actors.  Accounts can add their own threat actors if needed."""

    is_human = models.BooleanField(default=True, help_text=(
        'Designates whether this threat actor is a human'),)  # Determines if the threat actor is a human
    is_internal = models.BooleanField(default=False, help_text=(
        'Designates whether this threat actor internal to the company'),)  # Determines if the threat actor is internal to the company.
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


class ActorIntent(DefaultFieldsCategory):
    """Actor Input.  What intent might the threat Actor have on the Asset"""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Actor Intentions")


class ThreatActorIntent(DefaultFields):
    ''' Through table from Actor.  This table is used to tie threat actors to their intent.  '''
    id_actor = models.ForeignKey(
        Actor, on_delete=models.PROTECT,)  # Actor Id from the Actor table
    # ActorIntent Id from the ActorIntent table
    id_actorintent = models.ForeignKey(ActorIntent, on_delete=models.PROTECT,)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Threat Actor Intentions")


class ActorMotive(DefaultFieldsCategory):
    """Actor Motive."""

    def __str__(self):
        """String."""
        return self.name

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Actor Motives")


class ThreatActorMotive(DefaultFields):
    ''' Through table for Actor.  This table is used to tie threat actors to their motive.  '''
    id_actor = models.ForeignKey(
        Actor, on_delete=models.PROTECT)  # ActorId from the Actor table
    # ActorMotive Id from the ActorMotive table
    id_actormotive = models.ForeignKey(ActorMotive, on_delete=models.PROTECT)

    class Meta:
        """Meta class."""
        verbose_name_plural = ("Threat Actor Motives")
