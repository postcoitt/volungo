from django.urls import path
from . import views

urlpatterns = [
    path('my-button-action/', views.my_button_action, name='button_action'),
    path('show_filters/', views.filters_button_action, name = 'show_filters')
]
