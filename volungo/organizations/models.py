from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return str(self.name) if self.name else "Unnamed Tag"

class Organization(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizations', verbose_name="Власник")

    title = models.CharField(max_length=255, verbose_name="Назва")


    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    duration = models.CharField(max_length=50, verbose_name="Тривалість")
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0.0, verbose_name="Рейтинг"
    )
    description = models.TextField(verbose_name="Опис")


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Організація"
        verbose_name_plural = "Організації"
        ordering = ['-rating']

    def __str__(self):
        return str(self.title)
