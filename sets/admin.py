from django.contrib import admin
from .models import Set, Card, Card_closed_q, Card_answers

# Register your models here.
@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'description']
    raw_id_fields = ['owner']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['set', 'question', 'answer', 'card_nr', 'mastered_lvl', 'id', 'card_type']
    raw_id_fields = ['set']

@admin.register(Card_answers)
class CardAnswerAdmin(admin.ModelAdmin):
    list_display = ['parent_card', 'letter', 'is_correct']
    raw_id_fields = ['parent_card']