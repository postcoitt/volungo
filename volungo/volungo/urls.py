from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # apps
    path('', include('mapapp.urls')),
    path('', include('accounts.urls')),
    path('', include('users.urls'))
]
