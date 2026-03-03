from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва досягнення")
    icon_url = models.URLField(blank=True, verbose_name="Посилання на іконку")
    required_xp = models.PositiveIntegerField(default=0, verbose_name="Потрібно годин (XP)")
    def __str__(self): return self.name


class SkillTag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва бейджа (напр. 🌿 активний)")
    color = models.CharField(max_length=20, default="#14532d", verbose_name="Колір фону (HEX)")
    def __str__(self): return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, verbose_name="Про себе")
    badges = models.ManyToManyField(Badge, blank=True, verbose_name="Досягнення")
    skill_tags = models.ManyToManyField(SkillTag, blank=True, verbose_name="Бейджі під аватаркою")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Вік")
    xp = models.PositiveIntegerField(default=0, verbose_name="Години (XP)")
    level = models.CharField(max_length=50, default="Новачок", verbose_name="Рівень")

    def __str__(self): return self.user.username

    def save(self, *args, **kwargs):
        if self.xp < 50:
            self.level = "Новачок"
        elif 50 <= self.xp < 150:
            self.level = "Учасник"
        elif 150 <= self.xp < 500:
            self.level = "Просунутий"
        else:
            self.level = "Майстер"
        super().save(*args, **kwargs)

    def get_friends(self):
        """Returns queryset of UserProfiles that are confirmed friends."""
        sent = FriendRequest.objects.filter(
            from_user=self.user, status='accepted'
        ).values_list('to_user', flat=True)
        received = FriendRequest.objects.filter(
            to_user=self.user, status='accepted'
        ).values_list('from_user', flat=True)
        friend_ids = list(sent) + list(received)
        return UserProfile.objects.filter(user__in=friend_ids).select_related('user')

    def friends_count(self):
        return self.get_friends().count()


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending',  'Очікує'),
        ('accepted', 'Прийнято'),
        ('declined', 'Відхилено'),
    )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['from_user', 'to_user']

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.status})"


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва події")
    description = models.TextField(verbose_name="Опис")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг події")
    date = models.DateField(null=True, blank=True, verbose_name="Дата проведення")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Час початку")
    end_time = models.TimeField(null=True, blank=True, verbose_name="Час завершення")
    location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Локація (Де зустрічаємось?)")
    requirements = models.TextField(null=True, blank=True, verbose_name="Що взяти з собою? (кожний пункт з нового рядка)")
    program = models.TextField(null=True, blank=True, verbose_name="Програма або план дій")
    def __str__(self): return self.title


class HelperReview(models.Model):
    REVIEW_TYPES = (
        ('helper',   'Як помічнику'),
        ('organizer','Як організатору'),
    )
    volunteer   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_reviews')
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPES, default='helper', verbose_name="Тип відгуку")
    text        = models.TextField(verbose_name="Текст відгуку")
    rating      = models.IntegerField(default=5, verbose_name="Оцінка (1-5)")
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Відгук ({self.get_review_type_display()}) для {self.volunteer.username}"
