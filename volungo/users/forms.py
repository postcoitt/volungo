from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import HelperReview

User = get_user_model()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = HelperReview
        fields = ['review_type', 'rating', 'text']
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

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)
    email      = forms.EmailField()

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
