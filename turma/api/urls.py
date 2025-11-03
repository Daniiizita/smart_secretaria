from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TurmaViewSet  # troque "AlunoViewSet"

router = DefaultRouter()
router.register(r'', TurmaViewSet, basename='turma')  # '' = raiz da rota

urlpatterns = [
    path('', include(router.urls)),
]
