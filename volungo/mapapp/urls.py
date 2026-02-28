from django.urls import path
from . import views

urlpatterns = [
    path('my-button-action/', views.my_button_action, name='button_action'),
    path('show_filters/', views.filters_button_action, name='show_filters'),
    path('map/', views.interactive_map, name='map'),
    path('map/create/', views.create_event, name='create_event'),
    path('map/event/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('event/<int:event_id>/resolve/', views.event_resolve, name='event_resolve')
]
