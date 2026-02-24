from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ЦЕЙ БЛОК МАЄ БУТИ ПОВЕРНУТО:
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    xp = models.CharField(max_length=50, default="0/5000")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

# Твої сигнали (вони у тебе вже є, просто залиш їх нижче)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, full_name=instance.username)
