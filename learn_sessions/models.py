from django.db import models
from sets.models import Set
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Learn_session(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learn_sessions'
    )

    set=models.ForeignKey(
        Set,
        on_delete=models.CASCADE,
        related_name='learn_sessions'
    )

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now_add=True)

    current_card_nr = models.IntegerField(default=1)

    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f'Session {self.id} | {self.user} | {self.set.name}'
    
    