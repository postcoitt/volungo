from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=18)
    level = models.IntegerField(default=1)
    xp = models.CharField(max_length=20, default="0/5000")
    events_count = models.IntegerField(default=0)
    hours_count = models.IntegerField(default=0)
    friends_count = models.IntegerField(default=0)
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return self.user.username
