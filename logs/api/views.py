from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import LogAtividade  # troque "Aluno"
from .serializers import LogSerializer

class LogViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para CRUD completo do modelo.
    """
    queryset = LogAtividade.objects.all().order_by('id')  # ajuste a ordenação se precisar
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]  # exige JWT
