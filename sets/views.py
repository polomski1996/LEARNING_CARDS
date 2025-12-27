from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SetForm, CardForm
from .models import Set

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

login_required
def create_card(request, set_id):
    set_to_modify = get_object_or_404(
                Set,
                id=set_id,
                owner=request.user
            )
    
    if request.method == 'POST':
        form = CardForm(request.POST)
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
def delete_set(request, set_id):
    if request.method == 'POST':
        set_to_del = get_object_or_404(
            Set,
            id=set_id,
            owner=request.user
        )
        set_to_del.delete()

    return redirect('/account/')