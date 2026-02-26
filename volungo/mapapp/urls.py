from django.urls import path
from . import views

urlpatterns = [
    path('my-button-action/', views.my_button_action, name='button_action'),
    path('show_filters/', views.filters_button_action, name='show_filters'),
    path('map/', views.interactive_map, name='map'),
    path('map/create/', views.create_event, name='create_event'),
    path('map/event/<int:event_id>/', views.event_detail_view, name='event_detail'),
]
