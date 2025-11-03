from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet  # troque "AlunoViewSet"

router = DefaultRouter()
router.register(r'', CustomUserViewSet, basename='usuarios')  # '' = raiz da rota

urlpatterns = [
    path('', include(router.urls)),
]
