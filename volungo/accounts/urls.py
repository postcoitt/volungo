from django.contrib import admin
from django.urls import path, include

from . import views
'''urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('map/', include('mapapp.urls')),
    path('', include('users.urls')),  # ← add this
]
'''

urlpatterns = [
    path('login/', views.login_view, name='login'),
]
