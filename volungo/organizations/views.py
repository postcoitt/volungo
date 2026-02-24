import logging
from rest_framework import viewsets, permissions
from .models import Organization
from .serializers import OrganizationSerializer


logger = logging.getLogger(__name__)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Зберігаємо власника при створенні організації"""
        try:

            serializer.save(owner=self.request.user)
        except Exception as e:

            logger.error(f"Помилка при створенні організації користувачем {self.request.user}: {e}")
            raise

    def list(self, request, *args, **kwargs):
        """Обробка помилок при отриманні списку (наприклад, збій БД)"""
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Помилка отримання списку організацій: {e}")
            raise
