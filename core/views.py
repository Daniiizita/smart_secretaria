#core.views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

from aluno.models import Aluno
from professor.models import Professor
from turma.models import Turma
from matricula.models import Matricula
from calendario.models import Evento
from documentos.models import Documento
from logs.models import LogAtividade

def index(request):
    """
    View da página inicial (FBV = Function-Based View).
    - 'request' é obrigatório para qualquer view.
    - Retorna HTML renderizando o template com um contexto.
    """
    context = {"title": "SmartSecretaria", "subtitle": "Home Page"}
    return render(request, "core/index.html", context)

@login_required
def dashboard(request):
    """
    Dashboard principal do sistema, mostrando estatísticas e informações relevantes.
    """
    hoje = timezone.now()
    ano_atual = hoje.year
    mes_atual = hoje.month
    
    # Contagens gerais
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    total_turmas = Turma.objects.count()
    total_matriculas = Matricula.objects.filter(status='ativo').count()
    
    # Próximos eventos
    proximos_eventos = Evento.objects.filter(
        data_inicio__gte=hoje
    ).order_by('data_inicio')[:5]
    
    # Últimos alunos cadastrados
    ultimos_alunos = Aluno.objects.all().order_by('-id')[:5]
    
    # Últimas atividades do sistema
    ultimas_atividades = LogAtividade.objects.all().order_by('-data_hora')[:10]
    
    # Contadores adicionais
    documentos_mes_atual = Documento.objects.filter(
        data_emissao__year=ano_atual,
        data_emissao__month=mes_atual
    ).count()
    
    matriculas_ano_atual = Matricula.objects.filter(
        ano_letivo=ano_atual
    ).count()
    
    context = {
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'total_turmas': total_turmas,
        'total_matriculas': total_matriculas,
        'proximos_eventos': proximos_eventos,
        'ultimos_alunos': ultimos_alunos,
        'ultimas_atividades': ultimas_atividades,
        'documentos_mes_atual': documentos_mes_atual,
        'matriculas_ano_atual': matriculas_ano_atual,
    }
    
    return render(request, "core/dashboard.html", context)
