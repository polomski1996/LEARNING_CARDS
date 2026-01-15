from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Learn_session, Log_answer
from sets.models import Set, Card, Card_answers
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

#view that handles click on rate btn for open card
@require_POST
def rate_card(request):
    data = json.loads(request.body)

    card = Card.objects.get(
        id=data['card_id'],
        set__owner=request.user
    )
    old_mastered_lvl = card.mastered_lvl
    card.mastered_lvl = data['mastered_level']
    card.save(update_fields=['mastered_lvl'])

    #checking progress of mastered_lvl
    if int(card.mastered_lvl) > old_mastered_lvl:
        progress = 'BETTER'
    elif int(card.mastered_lvl) < old_mastered_lvl:
        progress = 'WORSE'
    else: progress = 'STILL'

    #log answer in Log_answers model
    session = Learn_session.objects.get(
        id=data['session_id'],
        set__owner=request.user
    )
    log = Log_answer.objects.create(session=session, type_of_card='open_card', logged_question=card.question,
                                    logged_answer=str(card.mastered_lvl), is_better=progress)
    log.save()

    return JsonResponse({'status': 'ok'})

#View that handles click on closed card answer
@require_POST
def judge_card(request):
    data = json.loads(request.body)
    answer = data['answer']

    card = Card.objects.get(
        id=data['card_id'],
        set__owner=request.user
    )

    ans_list = Card_answers.objects.filter(parent_card=card.id)

    #log answer in Log_answers model
    session = Learn_session.objects.get(
        id=data['session_id'],
        set__owner=request.user
    )
    log = Log_answer.objects.create(session=session, type_of_card='open_card', logged_question=card.question,
                    logged_answer=str(answer))
    
    for el in ans_list:
        if el.letter == answer:
            if el.is_correct == True:
                log.is_correct = True
                log.save()
                return JsonResponse({
                    "status": "ok",
                    "result": "correct"
                })
            elif el.is_correct == False:
                log.is_correct = False
                log.save()
                return JsonResponse({
                    "status": "ok",
                    "result": "incorrect"
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "invalid answer"
                })
    # FINISH IMPLEMENTATION!


@require_POST
def finish_session(request):
    try:
        data = json.loads(request.body)

        learning_session = Learn_session.objects.get(
            id=data['session_id'],
            user=request.user
        )

        learning_session.is_finished=True
        learning_session.finished_at=data['finished_at']
        learning_session.save(update_fields=['is_finished', 'finished_at'])

        return JsonResponse({
            'statis': 'ok',
            'message': 'session finished!'
        })

    except Learn_session.DoesNotExist:
        return JsonResponse({'error': 'Sesja nie istnieje'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@login_required
def results(request):
    learn_sessions = Learn_session.objects.order_by('-started_at')
    session_log = Log_answer.objects.order_by('-time_of_answer')

    return render(  
        request,
        'account/results.html',
        {
            'learn_sessions': learn_sessions,
            'session_log': session_log
        }
    )