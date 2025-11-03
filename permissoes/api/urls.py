from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerfilAcessoViewSet, TentativaLoginViewSet

router = DefaultRouter()
router.register(r'perfil-acesso', PerfilAcessoViewSet, basename='perfil-acesso')
router.register(r'tentativa-login', TentativaLoginViewSet, basename='tentativa-login')

urlpatterns = [
    path('', include(router.urls)),
]
