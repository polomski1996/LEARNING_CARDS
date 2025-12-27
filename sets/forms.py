from django import forms
from django.contrib.auth import get_user_model
from .models import Set, Card

#Set From
class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['name', 'description']

#Card Form
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['question', 'answer']