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
    
#Simple Card with open self rating model
class Card(models.Model):
    set = models.ForeignKey(
        Set,
        on_delete=models.CASCADE,
        related_name='cards'
    )
    question = models.TextField(blank=True)
    question_image = models.ImageField(
        upload_to='cards/questions/',
        blank=True,
        null=True
    )
    answer = models.TextField(blank=True)
    answer_image = models.ImageField(
        upload_to='cards/answers/',
        blank=True,
        null=True
    )


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
    
#Card with closed question.
class Card_closed_q(Card):
    pass

#Closed question card answers.
class Card_answers(models.Model):
    parent_card = models.ForeignKey(
        Card_closed_q,
        on_delete=models.CASCADE,
        related_name='card_answers'
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)