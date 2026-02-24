from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # Пароль буде потрібен ТІЛЬКИ тобі для адмінки
    path('', include('users.urls')), # Прибираємо 'api/', щоб посилання було прямим
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
