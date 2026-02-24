from django.shortcuts import render

def profile_view(request, username):
    context = {
        'username': username,
        'full_name': username,
        'age': 30,
        'level': 12,
        'xp': '3400/5000',
        # Тимчасові посилання на фото (можете замінити на свої)
        'avatar_url': 'https://i.imgur.com/8Km9tLL.png',
        'org_logo': 'https://i.imgur.com/he9S6y8.png'
    }
    return render(request, 'users/profile.html', context)
