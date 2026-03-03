from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event, EventRegistration
from django.db.models import Avg
from django.utils import timezone

def my_button_action(request):
    result = {"message": 'Кнопка натиснулась і працює! Слава Богу!'}
    return JsonResponse(result)


def filters_button_action(request):
    filters = [
        {"filter1": "filter", "text": "Button"},
        {"filter2": "filter", "text": "Button"},
        {"filter3": "filter", "text": "Button"}
               ]
    return JsonResponse({"buttfiltersons": filters})

@login_required
def interactive_map(request):
    from django.db.models import Avg
    from users.models import HelperReview
    from django.utils import timezone

    events = Event.objects.filter(is_completed=False).select_related('organiser')
    for event in events:
        event.organiser_avg_rating = HelperReview.objects.filter(
            volunteer=event.organiser,
            review_type='organizer'
        ).aggregate(Avg('rating'))['rating__avg']

    # IDs of events the current user registered for
    registered_ids = list(
        EventRegistration.objects.filter(user=request.user)
        .values_list('event_id', flat=True)
    ) if request.user.is_authenticated else []

    # Expired events this organiser hasn't resolved yet
    expired_events = Event.objects.filter(
        organiser=request.user,
        is_completed=False,
        datetime__lt=timezone.now()
    ) if request.user.is_authenticated else []

    return render(request, 'mapapp/map.html', {
        'events': events,
        'registered_ids': registered_ids,
        'expired_events': expired_events,
    })

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')

        if form.is_valid() and lat and lng:
            event = form.save(commit=False)
            event.organiser  = request.user
            event.latitude   = float(lat)
            event.longitude  = float(lng)
            event.save()
            return redirect('map')

        # if location missing, re-render with error
        return render(request, 'mapapp/create_event.html', {
            'form': form,
            'location_error': not (lat and lng)
        })

    form = EventForm()
    return render(request, 'mapapp/create_event.html', {'form': form})


def event_detail_view(request, event_id):
    from mapapp.models import Event as MapEvent, EventRegistration, EventReview
    from users.models import UserProfile
    from django.db.models import Avg

    event = get_object_or_404(MapEvent, id=event_id)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(
            event=event, user=request.user
        ).exists()

    organizer_profile, _ = UserProfile.objects.get_or_create(user=event.organiser)

    organiser_events = MapEvent.objects.filter(organiser=event.organiser, is_completed=True)
    event_avgs = []
    for ev in organiser_events:
        avg = EventReview.objects.filter(event=ev).aggregate(Avg('rating'))['rating__avg']
        if avg:
            event_avgs.append(avg)
    avg_organiser_rating = round(sum(event_avgs) / len(event_avgs), 1) if event_avgs else None

    # Відгуки волонтерів на подію
    reviews = EventReview.objects.filter(event=event).select_related('author').order_by('-created_at')

    # Чи вже залишив відгук поточний користувач
    user_already_reviewed = False
    if request.user.is_authenticated:
        user_already_reviewed = EventReview.objects.filter(
            event=event, author=request.user
        ).exists()

    # Обробка форми відгуку
    if request.method == 'POST' and request.user.is_authenticated:
        if is_registered and event.is_completed and not user_already_reviewed:
            rating = int(request.POST.get('rating', 5))
            text   = request.POST.get('text', '').strip()
            if text and 1 <= rating <= 5:
                EventReview.objects.create(
                    event=event,
                    author=request.user,
                    rating=rating,
                    text=text,
                )
        return redirect('event_detail', event_id=event_id)

    return render(request, 'users/events/event.html', {
        'event': event,
        'is_registered': is_registered,
        'organizer_profile': organizer_profile,
        'reviews': reviews,
        'user_already_reviewed': user_already_reviewed,
        'avg_organiser_rating': avg_organiser_rating,
        'can_review': is_registered and event.is_completed and not user_already_reviewed,
    })

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reg, created = EventRegistration.objects.get_or_create(event=event, user=request.user)
    if not created:
        reg.delete()  # toggle — if already registered, unregister
    return redirect('event_detail', event_id=event_id)

@login_required
def event_resolve(request, event_id):
    event = get_object_or_404(Event, id=event_id, organiser=request.user)
    registrations = EventRegistration.objects.filter(event=event).select_related('user')

    if request.method == 'POST':
        from users.models import UserProfile, HelperReview
        for reg in registrations:
            uid = str(reg.user.id)
            hours  = int(request.POST.get(f'hours_{uid}', 0))
            rating = int(request.POST.get(f'rating_{uid}', 0))
            text   = request.POST.get(f'text_{uid}', '').strip()

            if hours > 0:
                profile, _ = UserProfile.objects.get_or_create(user=reg.user)
                profile.xp += hours
                profile.save()

            if rating > 0 and text:
                HelperReview.objects.create(
                    volunteer=reg.user,
                    author=request.user,
                    review_type='helper',
                    rating=rating,
                    text=text,
                    event=event
                )

        event.is_completed = True
        event.save()
        return redirect('map')

    return render(request, 'mapapp/event_resolve.html', {
        'event': event,
        'registrations': registrations,
    })
