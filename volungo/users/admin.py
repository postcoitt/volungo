from django.contrib import admin
from .models import SkillTag
from .models import UserProfile, Badge, Event, HelperReview

# Реєструємо наші моделі, щоб вони з'явилися в адмінці
admin.site.register(UserProfile)
admin.site.register(Badge)
admin.site.register(Event)
admin.site.register(HelperReview)

admin.site.register(SkillTag)
