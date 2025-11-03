from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessorViewSet  # troque "AlunoViewSet"

router = DefaultRouter()
router.register(r'', ProfessorViewSet, basename='professor')  # '' = raiz da rota

urlpatterns = [
    path('', include(router.urls)),
]
