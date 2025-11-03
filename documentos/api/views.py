from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Documento # troque "Aluno"
from .serializers import DocumentoSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para CRUD completo do modelo.
    """
    queryset = Documento.objects.all().order_by('id')  # ajuste a ordenação se precisar
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]  # exige JWT
