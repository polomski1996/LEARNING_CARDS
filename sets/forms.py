from django import forms
from django.contrib.auth import get_user_model
from .models import Set, Card, Card_closed_q, Card_answers
from django.forms import modelformset_factory

#Set From
class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['name', 'description']

#Card Form
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['question', 'question_image', 'answer', 'answer_image']

    def clean(self):
        cleaned = super().clean()

        if not (
            cleaned.get('question') or cleaned.get('question_image')
        ):
            raise forms.ValidationError(
                "Question must have text or image"
            )

        if not (
            cleaned.get('answer') or cleaned.get('answer_image')
        ):
            raise forms.ValidationError(
                "Answer must have text or image"
            )

        return cleaned

#Card Form
class ClosedCardForm(forms.ModelForm):
    class Meta:
        model = Card_closed_q
        fields = ['question', 'question_image']

    def clean(self):
        cleaned = super().clean()

        if not (
            cleaned.get('question') or cleaned.get('question_image')
        ):
            raise forms.ValidationError(
                "Question must have text or image"
            )

        return cleaned

#Answers for ClosedCardForm
class AnswersClosedCardForm(forms.ModelForm):
    class Meta:
        model = Card_answers
        fields = ['letter', 'is_correct']
        extra=6
        can_delete=False