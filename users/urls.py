from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('my-profile/', views.my_profile_redirect, name='my_profile'),
    path('test-event/', views.test_event_view, name='test_event'),
]
