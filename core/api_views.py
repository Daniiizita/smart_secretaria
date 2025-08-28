# filepath: /home/gonca/smart_secretaria/core/api_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from aluno.models import Aluno
from professor.models import Professor
from turma.models import Turma
from documentos.models import Documento
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

@login_required
def busca_rapida_api(request):
    """
    Endpoint de API para busca rápida, retorna resultados em formato JSON.
    Para uso com AJAX na interface.
    """
    query = request.GET.get('q', '')
    resultados = {
        'alunos': [],
        'professores': [],
        'turmas': [],
        'documentos': [],
        'eventos': []
    }
    
    if query and len(query) >= 3:  # Mínimo de 3 caracteres
        # Busca em Alunos
        alunos = Aluno.objects.filter(
            Q(nome_completo__icontains=query) |
            Q(cpf__icontains=query) |
            Q(email__icontains=query)
        ).order_by('nome_completo')[:5]  # Limitar a 5 resultados para busca rápida
        
        resultados['alunos'] = [{'id': a.id, 'nome_completo': a.nome_completo} for a in alunos]
        
        # Busca em Professores
        professores = Professor.objects.filter(
            Q(nome__icontains=query) |
            Q(email__icontains=query) |
            Q(disciplina__icontains=query)
        ).order_by('nome')[:5]
        
        resultados['professores'] = [{'id': p.id, 'nome': p.nome} for p in professores]
        
        # Busca em Turmas
        turmas = Turma.objects.filter(
            Q(nome__icontains=query) |
            Q(sala__icontains=query) |
            Q(periodo__icontains=query)
        ).order_by('nome')[:5]
        
        resultados['turmas'] = [{'id': t.id, 'nome': t.nome} for t in turmas]
        
    return JsonResponse(resultados)