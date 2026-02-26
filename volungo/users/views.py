# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import CustomUserCreationForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Event, HelperReview, Badge, SkillTag
from .forms import CustomUserCreationForm, ReviewForm  # Тепер імпортуємо кастомну форму

# === Функція для перевірки та додавання бейджів ===
def check_and_assign_badges(profile):
    all_badges = Badge.objects.all()
    for badge in all_badges:
        if profile.xp >= badge.required_xp:
            if badge not in profile.badges.all():
                profile.badges.add(badge)
    profile.save()

# === Сторінка користувача ===
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=profile_user)

    if request.method == 'POST':
        if 'avatar' in request.FILES and request.user.is_authenticated:
            if request.user == profile_user:
                profile.avatar = request.FILES['avatar']
                profile.save()
            return redirect('user_profile', username=username)

        elif 'action' in request.POST and request.POST['action'] == 'add_hours':
            auth_user, auth_pass = request.POST.get('auth_username'), request.POST.get('auth_password')
            hours = int(request.POST.get('hours', 0))
            valid_user = authenticate(request, username=auth_user, password=auth_pass)

            if valid_user:
                if valid_user == profile_user:
                    messages.error(request, "Ви не можете самостійно додати собі годин!")
                else:
                    if hours > 0:
                        profile.xp += hours
                        profile.save()
                        check_and_assign_badges(profile)
                        messages.success(request, f"Успішно додано {hours} годин!")
            else:
                messages.error(request, "Неправильне ім'я користувача або пароль.")
            return redirect('user_profile', username=username)

        elif 'action' in request.POST and request.POST['action'] == 'add_friend':
            messages.success(request, f"Користувача {profile_user.username} успішно додано до друзів!")
            return redirect('user_profile', username=username)

        elif 'action' in request.POST and request.POST['action'] == 'add_badge':
            auth_user, auth_pass = request.POST.get('auth_username'), request.POST.get('auth_password')
            tag_id = request.POST.get('tag_id')
            valid_user = authenticate(request, username=auth_user, password=auth_pass)

            if valid_user:
                if valid_user == profile_user:
                    messages.error(request, "Ви не можете самостійно додати собі бейдж!")
                elif tag_id:
                    tag = get_object_or_404(SkillTag, id=tag_id)
                    profile.skill_tags.add(tag)
                    messages.success(request, f"Бейдж '{tag.name}' успішно додано!")
            else:
                messages.error(request, "Неправильне ім'я користувача або пароль.")
            return redirect('user_profile', username=username)

        elif 'action' in request.POST and request.POST['action'] == 'add_review' and request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.volunteer = profile_user
                review.author = request.user
                review.save()
                messages.success(request, "Відгук успішно додано!")
                return redirect('user_profile', username=username)

    if 'form' not in locals():
        form = ReviewForm()

    check_and_assign_badges(profile)

    helper_reviews = HelperReview.objects.filter(volunteer=profile_user, review_type='helper').order_by('-created_at')
    organizer_reviews = HelperReview.objects.filter(volunteer=profile_user, review_type='organizer').order_by('-created_at')
    available_tags = SkillTag.objects.all()
    avg_rating = HelperReview.objects.filter(volunteer=profile_user).aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    context = {
        'avg_rating': avg_rating,
        'profile_user': profile_user,
        'profile': profile,
        'badges': profile.badges.all(),
        'skill_tags': profile.skill_tags.all(),
        'available_tags': available_tags,
        'helper_reviews': helper_reviews,
        'organizer_reviews': organizer_reviews,
        'form': form,
    }
    return render(request, 'users/profile.html', context)

# === Реєстрація нового користувача ===
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # <- використовується кастомна форма
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('my_profile')
    else:
        form = CustomUserCreationForm()  # <- і тут теж кастомна форма

    return render(request, 'users/register.html', {'form': form})

# === Перенаправлення на свій профіль ===
@login_required
def my_profile_redirect(request):
    return redirect('profile', username=request.user.username)


# === РОЗУМНЕ ПЕРЕНАПРАВЛЕННЯ НА СВІЙ ПРОФІЛЬ ===
@login_required
def my_profile(request):
    # Ця функція бере логін поточного користувача і кидає його на його ж сторінку
    return redirect('user_profile', username=request.user.username)

def test_event_view(request):
    from mapapp.models import Event as MapEvent
    event = MapEvent.objects.first()
    return render(request, 'users/events/event.html', {'event': event})
