from django.urls import path
from . import views

urlpatterns = [
    # Тепер адреса буде просто: 127.0.0.1:8000/Olesia/
    path('<str:username>/', views.profile_view, name='profile'),
]

