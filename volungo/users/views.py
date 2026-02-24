from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

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
