from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SetForm, CardForm, ClosedCardForm, AnswersClosedCardForm
from .models import Set, Card_answers

# Create your views here.

@login_required
def create_set(request):
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            set_obj = form.save(commit=False)
            set_obj.owner = request.user
            set_obj.save()
        return redirect('/account/')
    else:
        form = SetForm()

    return render(request, 'sets/create_set.html', {'form': form})

@login_required
def create_card(request, set_id):
    set_to_modify = get_object_or_404(
                Set,
                id=set_id,
                owner=request.user
            )
    
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.set = set_to_modify
            card.save()
            return redirect('/account/')
    else:
        form = CardForm()

    return render(
        request,
        'sets/create_card.html',
        {
            'form': form,
            'set': set_to_modify
        }
    )

@login_required
def create_closed_card(request, set_id):
    set_to_modify = get_object_or_404(
            Set,
            id=set_id,
            owner=request.user
        )
    
    if request.method == 'POST':
        form_q = ClosedCardForm(request.POST, request.FILES)
        if form_q.is_valid():
            closed_question = form_q.save(commit=False)
            closed_question.set = set_to_modify
            closed_question.save()
            
            answers_count = int(request.POST.get('answers_count', 0))

            for i in range(answers_count):
                letter = request.POST.get(f'letter_{i}')
                is_correct = request.POST.get(f'is_correct_{i}') == 'on'
                
                Card_answers.objects.create(
                    parent_card=closed_question,
                    letter=letter,
                    is_correct=is_correct
                )
            return redirect('/account/')
    else:
        form_q = ClosedCardForm()

    return render(
        request,
        'sets/create_closed_card.html',
        {
            'form_q': form_q,
            'set': set_to_modify
        }
    )

@login_required
def delete_set(request, set_id):
    if request.method == 'POST':
        set_to_del = get_object_or_404(
            Set,
            id=set_id,
            owner=request.user
        )
        set_to_del.delete()

    return redirect('/account/')