from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogViewSet  # troque "AlunoViewSet"

router = DefaultRouter()
router.register(r'', LogViewSet, basename='logs')  # '' = raiz da rota

urlpatterns = [
    path('', include(router.urls)),
]
