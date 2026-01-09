from django.urls import path
from . import views

app_name = 'learn_sessions'

urlpatterns = [
    path(
        'start/<int:set_id>/',
        views.start_session,
        name='start',
    ),
    path(
        'session/<int:session_id>/',
        views.learn_session_view,
        name='session',
    ),
    path(
        'api/rate-card/',
        views.rate_card,
        name='rate_card',
    ),
    path(
        'api/finish_session/',
        views.finish_session,
        name='finish_session',
    ),
    path(
        'api/judge-answer/',
        views.judge_card,
        name='judge-answer'
    )
]