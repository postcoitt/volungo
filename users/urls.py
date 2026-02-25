from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('my-profile/', views.my_profile_redirect, name='my_profile'),
    path('test-event/', views.test_event_view, name='test_event'),
=======
    # Сторінки входу та реєстрації
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Розумний редирект на свій профіль
    path('my-profile/', views.my_profile, name='my_profile'),

    # Твоя сторінка профілю (має бути в самому кінці!)
    path('<str:username>/', views.user_profile, name='user_profile'),
>>>>>>> yatsko/user_page
]
