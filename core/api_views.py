# filepath: /home/gonca/smart_secretaria/core/api_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from aluno.models import Aluno
from professor.models import Professor
from calendario.models import Evento
from .serializers import AlunoSerializer, ProfessorSerializer, EventoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated]

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]