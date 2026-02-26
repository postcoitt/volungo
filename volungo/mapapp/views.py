from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event

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

def interactive_map(request):
    events = Event.objects.all()
    return render(request, 'mapapp/map.html', {'events': events})

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
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'users/events/event.html', {'event': event})
