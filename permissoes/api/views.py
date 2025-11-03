from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import PerfilAcesso, TentativaLogin  # troque "Aluno"
from .serializers import PerfilAcessoSerializer, TentativaLoginSerializer

class PerfilAcessoViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para CRUD completo do modelo.
    """
    queryset = PerfilAcesso.objects.all().order_by('id')  # ajuste a ordenação se precisar
    serializer_class = PerfilAcessoSerializer
    permission_classes = [IsAuthenticated]  # exige JWT

class TentativaLoginViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para CRUD completo do modelo.
    """
    queryset = TentativaLogin.objects.all().order_by('id')  # ajuste a ordenação se precisar
    serializer_class =  TentativaLoginSerializer
    permission_classes = [IsAuthenticated]  # exige JW