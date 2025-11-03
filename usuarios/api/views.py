from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import CustomUser  # troque "Aluno"
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para CRUD completo do modelo.
    """
    queryset = CustomUser.objects.all().order_by('id')  # ajuste a ordenação se precisar
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # exige JWT
