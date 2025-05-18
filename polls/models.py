from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    
    # Required for Django's auth system
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

class Poll(models.Model):
    question = models.CharField(max_length=200)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    closes_at = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    allow_multiple_votes = models.BooleanField(default=False)

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    @property
    def votes_percentage(self):
        total = self.poll.choice_set.aggregate(total=Sum('votes'))['total']
        return round((self.votes / total) * 100, 2) if total else 0

class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)