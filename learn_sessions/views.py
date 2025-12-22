from django.shortcuts import render, get_object_or_404, redirect
from .models import Learn_session
from sets.models import Set

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

    return redirect('learn_session:session', session.id)

def learn_session_view(request, session_id):
    session = get_object_or_404(
        Learn_session,
        id=session_id,
        user=request.user
    )

    cards = session.set.cards.all()

    return render(request, 'learning_sessions/learn_session.html', {
        'session', session,
        'cards', cards,
    })
