from django.shortcuts import render, get_object_or_404
from .models import Profile

def profile_view(request, username):
    # Шукаємо профіль у базі даних за ім'ям користувача
    profile = get_object_or_404(Profile, user__username=username)

    context = {
        'full_name': profile.full_name,
        'age': profile.age,
        'level': profile.level,
        'xp': profile.xp,
        'avatar_url': profile.avatar.url if profile.avatar else 'https://i.imgur.com/8Km9tLL.png',
    }
    return render(request, 'users/profile.html', context)
