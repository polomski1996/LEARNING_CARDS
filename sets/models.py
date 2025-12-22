from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Set(models.Model):
    owner=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sets' 
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sessions_count = models.PositiveIntegerField(default=0, editable=False)

    @property
    def cards_count(self):
        """Return ammount of cards present in the Set"""
        return self.cards.count()

    def __str__(self):
        return self.name
    
class Card(models.Model):
    set = models.ForeignKey(
        Set,
        on_delete=models.CASCADE,
        related_name='cards'
    )
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    card_nr = models.PositiveIntegerField(default=1, editable=False)
    mastered_lvl = models.PositiveSmallIntegerField(default=0)

    #automatic sort by  card_nr
    class Meta:
        ordering = ['card_nr']

    def save(self, *args, **kwargs):
        """Automate assigning number of a card during creating it"""
        if not self.pk:
            last_card = Card.objects.filter(set=self.set).order_by('-card_nr').first()
            if last_card:
                self.card_nr = last_card.card_nr + 1
            else:
                self.card_nr = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question[:40]