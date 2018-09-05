"""All views related to Compliance in models/compliance.py."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from risk.models import (
    Actor,
    ActorIntent,
    ActorMotive,
)


@login_required
def get_all_actors_for_dropdown(request):
    """Get all actors for dropdown."""
    data = {}
    # for actor in Actor.objects.filter().all():
    for actor in Actor.objects.filter().all():
        data.update({actor.id: actor.name})

    return JsonResponse(data)


@login_required
def get_all_actor_intents_for_dropdown(request):
    """Get all actor intent for dropdown."""
    data = {}
    # for actor_intent in ActorIntent.objects.filter().all():
    for actor_intent in ActorIntent.objects.filter().all():
        data.update({actor_intent.id: actor_intent.name})

    return JsonResponse(data)


@login_required
def get_all_actor_motives_for_dropdown(request):
    """Get all actor motive for dropdown."""
    data = {}
    # for actor_motive in ActorMotive.objects.filter().all():
    for actor_motive in ActorMotive.objects.filter().all():
        data.update({actor_motive.id: actor_motive.name})

    return JsonResponse(data)

