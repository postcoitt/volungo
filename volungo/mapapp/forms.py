from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=Event.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'datetime', 'duration', 'max_volunteers', 'categories']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration <= 0:
            raise forms.ValidationError('Тривалість має бути більше 0.')
        return duration

    def clean_max_volunteers(self):
        max_v = self.cleaned_data.get('max_volunteers')
        if max_v < 1:
            raise forms.ValidationError('Має бути щонайменше 1 волонтер.')
        return max_v
