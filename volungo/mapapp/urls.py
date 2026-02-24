from django.urls import path
from . import views

urlpatterns = [
    path('my-button-action/', views.my_button_action, name='button_action'),
    path('show_filters/', views.filters_button_action, name = 'show_filters'),
    path('map/', views.interactive_map, name="map"),
    path('new_page/', views.more_details, name="details"),
]
