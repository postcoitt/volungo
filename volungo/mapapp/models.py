from django.db import models

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('animals',   'Допомога тваринам'),
        ('nets',      'Плетіння сіток для армії'),
        ('shelter',   'Допомога в пансіонаті'),
        ('food',      'Приготування теплих страв'),
        ('cleanup',   'Прибирання території'),
        ('children',  'Робота з дітьми'),
        ('elderly',   'Допомога літнім людям'),
        ('medical',   'Медична допомога'),
        ('transport', 'Транспортна допомога'),
        ('other',     'Інше'),
    ]

    organiser       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    name            = models.CharField(max_length=200)
    description     = models.TextField()
    datetime        = models.DateTimeField()
    duration        = models.FloatField(help_text='Duration in hours')
    max_volunteers  = models.PositiveIntegerField()
    categories      = models.JSONField(default=list)
    latitude        = models.FloatField()
    longitude       = models.FloatField()
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
