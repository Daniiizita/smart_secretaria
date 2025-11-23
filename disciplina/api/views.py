from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from disciplina.models import Disciplina
from .serializers import DisciplinaSerializer

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all().order_by('id')
    serializer_class = DisciplinaSerializer
    permission_classes = [IsAuthenticated]