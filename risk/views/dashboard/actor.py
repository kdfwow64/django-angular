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
    data = []
    for actor in Actor.objects.order_by('name').all():
        data.append({'id': actor.id, 'name': actor.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_actor_intents_for_dropdown(request):
    """Get all actor intent for dropdown."""
    data = []
    for actor_intent in ActorIntent.objects.order_by('name').all():
        data.append({'id': actor_intent.id, 'name': actor_intent.name})
    return JsonResponse(data, safe=False)


@login_required
def get_all_actor_motives_for_dropdown(request):
    """Get all actor motive for dropdown."""
    data = []
    for actor_motive in ActorMotive.objects.order_by('name').all():
        data.append({'id': actor_motive.id, 'name': actor_motive.name})
    return JsonResponse(data, safe=False)

