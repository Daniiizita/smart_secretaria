from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Notificacao  # troque "Aluno"
from .serializers import NotificacaoSerializer

class NotificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para CRUD completo do modelo.
    """
    queryset = Notificacao.objects.all().order_by('id')  # ajuste a ordenação se precisar
    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]  # exige JWT
