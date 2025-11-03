from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatriculaViewSet  # troque "AlunoViewSet"

router = DefaultRouter()
router.register(r'', MatriculaViewSet, basename='matricula')  # '' = raiz da rota

urlpatterns = [
    path('', include(router.urls)),
]
