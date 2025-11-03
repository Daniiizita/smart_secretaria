from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Matricula  # troque "Aluno"
from .serializers import MatriculaSerializer

class MatriculaViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para CRUD completo do modelo.
    """
    queryset = Matricula.objects.all().order_by('id')  # ajuste a ordenação se precisar
    serializer_class = MatriculaSerializer
    permission_classes = [IsAuthenticated]  # exige JWT
