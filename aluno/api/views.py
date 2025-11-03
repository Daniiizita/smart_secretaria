from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from aluno.models import Aluno
from .serializers import AlunoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all().order_by('nome_completo')
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated]
