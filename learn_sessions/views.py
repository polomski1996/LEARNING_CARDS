from django.shortcuts import render, get_object_or_404, redirect
from .models import Learn_session
from sets.models import Set, Card
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse

# Create your views here.
def start_session(request, set_id):
    set_obj = get_object_or_404(
        Set,
        id=set_id,
        owner=request.user
    )

    session = Learn_session.objects.create(
        user=request.user,
        set=set_obj
    )

    return redirect('learn_sessions:session', session.id)

def learn_session_view(request, session_id):
    session = get_object_or_404(
        Learn_session,
        id=session_id,
        user=request.user
    )

    cards = session.set.cards.all()

    return render(request, 'learn_sessions/learn_session.html', {
        'session': session,
        'cards': cards,
    })

@require_POST
def rate_card(request):
    data = json.loads(request.body)

    card = Card.objects.get(
        id=data['card_id'],
        set__owner=request.user
    )

    card.mastered_lvl = data['mastered_level']
    card.save(update_fields=['mastered_lvl'])

    return JsonResponse({'status': 'ok'})