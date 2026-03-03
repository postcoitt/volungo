from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from .forms import CustomUserCreationForm, ReviewForm
from .models import UserProfile, Event, HelperReview, Badge, SkillTag, FriendRequest
from mapapp.models import EventRegistration

def check_and_assign_badges(profile):
    for badge in Badge.objects.all():
        if profile.xp >= badge.required_xp and badge not in profile.badges.all():
            profile.badges.add(badge)
    profile.save()


def _get_friend_status(viewer, target):
    """
    Returns one of: 'self', 'friends', 'request_sent', 'request_received', 'none'
    viewer and target are User instances.
    """
    if viewer == target:
        return 'self'
    # sent by viewer
    req = FriendRequest.objects.filter(from_user=viewer, to_user=target).first()
    if req:
        if req.status == 'accepted': return 'friends'
        if req.status == 'pending':  return 'request_sent'
    # sent by target
    req = FriendRequest.objects.filter(from_user=target, to_user=viewer).first()
    if req:
        if req.status == 'accepted':  return 'friends'
        if req.status == 'pending':   return 'request_received'
    return 'none'


def user_profile(request, username):
    from mapapp.models import Event as MapEvent, EventRegistration
    from django.db.models import Avg

    profile_user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if 'avatar' in request.FILES and request.user.is_authenticated and request.user == profile_user:
            profile.avatar = request.FILES['avatar']
            profile.save()
            return redirect('user_profile', username=username)

        if action == 'send_friend_request' and request.user.is_authenticated:
            if request.user != profile_user:
                FriendRequest.objects.get_or_create(
                    from_user=request.user, to_user=profile_user,
                    defaults={'status': 'pending'}
                )
            return redirect('user_profile', username=username)

        if action == 'remove_friend' and request.user.is_authenticated:
            from django.db.models import Q
            FriendRequest.objects.filter(
                Q(from_user=request.user, to_user=profile_user) |
                Q(from_user=profile_user, to_user=request.user)
            ).delete()
            return redirect('user_profile', username=username)

        if action == 'add_review' and request.user.is_authenticated:
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

    friend_status = 'self'
    if request.user.is_authenticated:
        friend_status = _get_friend_status(request.user, profile_user)

    # ── Events as organiser ──
    organised_events = MapEvent.objects.filter(organiser=profile_user).order_by('-datetime')
    organised_data = []
    for ev in organised_events:
        avg = HelperReview.objects.filter(
            event=ev, review_type='organizer'
        ).aggregate(Avg('rating'))['rating__avg']
        organised_data.append({
            'event': ev,
            'avg_rating': round(avg, 1) if avg else None,
            'volunteer_count': ev.registrations.count(),
        })

    # ── Events as volunteer (participated) ──
    participated_regs = EventRegistration.objects.filter(
        user=profile_user,
        event__is_completed=True
    ).select_related('event').order_by('-event__datetime')

    participated_data = []
    for reg in participated_regs:
        review = HelperReview.objects.filter(
            event=reg.event,
            volunteer=profile_user,
            review_type='helper'
        ).first()
        participated_data.append({
            'event': reg.event,
            'review': review,
        })

    avg_rating = HelperReview.objects.filter(volunteer=profile_user).aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    context = {
        'avg_rating': avg_rating,
        'profile_user': profile_user,
        'profile': profile,
        'badges': profile.badges.all(),
        'skill_tags': profile.skill_tags.all(),
        'available_tags': SkillTag.objects.all(),
        'form': form,
        'friend_status': friend_status,
        'friends_count': profile.friends_count(),
        'organised_data': organised_data,
        'participated_data': participated_data,
    }
    return render(request, 'users/profile.html', context)


@login_required
def accept_friend_request(request, request_id):
    freq = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, status='pending')
    freq.status = 'accepted'
    freq.save()
    messages.success(request, f"Ви тепер друзі з {freq.from_user.username}!")
    return redirect('friends_list', username=request.user.username)


@login_required
def decline_friend_request(request, request_id):
    freq = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, status='pending')
    freq.delete()
    return redirect('friends_list', username=request.user.username)


def friends_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)

    confirmed_profiles = profile.get_friends()
    friends_data = []
    for f in confirmed_profiles:
        avg = HelperReview.objects.filter(volunteer=f.user).aggregate(Avg('rating'))['rating__avg']
        friends_data.append({
            'profile': f,
            'avg_rating': round(avg, 1) if avg else 0,
        })

    # Pending requests TO this user — only shown to the user themselves
    pending_requests = []
    if request.user.is_authenticated and request.user == profile_user:
        pending_requests = FriendRequest.objects.filter(
            to_user=profile_user, status='pending'
        ).select_related('from_user', 'from_user__profile')

    return render(request, 'users/friends.html', {
        'profile_user': profile_user,
        'friends_data': friends_data,
        'pending_requests': pending_requests,
        'is_own_page': request.user.is_authenticated and request.user == profile_user,
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('my_profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def my_profile_redirect(request):
    return redirect('profile', username=request.user.username)


@login_required
def my_profile(request):
    return redirect('user_profile', username=request.user.username)


def test_event_view(request):
    from mapapp.models import Event as MapEvent
    event = MapEvent.objects.first()
    return render(request, 'users/events/event.html', {'event': event})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(HelperReview, id=review_id)
    if review.author == request.user:
        username = review.volunteer.username
        review.delete()
        return redirect('user_profile', username=username)
    return redirect('map')
