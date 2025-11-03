from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from aluno.models import Aluno
from .serializers import AlunoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all().order_by('id')
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated]
