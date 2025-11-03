from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Turma  # troque "Aluno"
from .serializers import TurmaSerializer

class TurmaViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para CRUD completo do modelo.
    """
    queryset = Turma.objects.all().order_by('id')  # ajuste a ordenação se precisar
    serializer_class = TurmaSerializer
    permission_classes = [IsAuthenticated]  # exige JWT
