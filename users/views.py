from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def profile_view(request, username):
    # Шукаємо профіль у базі даних за ім'ям користувача
    user = User.objects.get(username=username)
    profile = user.profile

    context = {
        'full_name': profile.full_name,
        'age': profile.age,
        'level': profile.level,
        'xp': profile.xp,
        'avatar_url': profile.avatar.url if profile.avatar else 'https://i.imgur.com/8Km9tLL.png',
    }
    return render(request, 'users/profile.html', context)


@login_required
def my_profile_redirect(request):
    return redirect('profile', username=request.user.username)
