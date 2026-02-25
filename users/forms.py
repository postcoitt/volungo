from django import forms
from .models import HelperReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = HelperReview
        fields = ['review_type', 'rating', 'text'] # Додали review_type
        widgets = {
            'review_type': forms.Select(attrs={'style': 'width: 100%; padding: 8px; border-radius: 6px; margin-bottom: 10px;'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'style': 'width: 60px; padding: 5px; margin-bottom: 10px;'}),
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишіть ваш відгук тут...', 'style': 'width: 100%; border-radius: 8px; padding: 10px;'}),
        }
        labels = {
            'review_type': 'Кого ви оцінюєте?',
            'rating': 'Оцінка (1-5)',
            'text': 'Ваш відгук'
        }
