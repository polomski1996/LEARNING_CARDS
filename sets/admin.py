from django.contrib import admin
from .models import Set, Card

# Register your models here.
@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'description']
    raw_id_fields = ['owner']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['set', 'question', 'answer', 'card_nr', 'mastered_lvl']
    raw_id_fields = ['set']