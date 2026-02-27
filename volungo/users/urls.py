from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('my-profile/', views.my_profile_redirect, name='my_profile'),
    path('test-event/', views.test_event_view, name='test_event'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
