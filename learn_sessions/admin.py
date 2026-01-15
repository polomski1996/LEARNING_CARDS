from django.contrib import admin
from .models import Learn_session, Log_answer

# Register your models here.
@admin.register(Learn_session)
class Learn_sesssionAdmin(admin.ModelAdmin):
    list_display = ['user', 'set', 'started_at', 'finished_at', 'is_finished']
    raw_id_fields = ['user']

@admin.register(Log_answer)
class Log_answerAdmin(admin.ModelAdmin):
    list_display = ['session', 'time_of_answer', 'type_of_card', 'logged_question', 'logged_answer', 'is_correct', 'is_better']
    raw_id_fields = ['session']