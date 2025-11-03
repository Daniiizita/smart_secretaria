#core.views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from aluno.models import Aluno
from professor.models import Professor
from turma.models import Turma
from matricula.models import Matricula
from calendario.models import Evento
from documentos.models import Documento
from logs.models import LogAtividade

from notificacoes.utils import criar_notificacoes_eventos

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
    
    # Gerar notificações automaticamente
    criar_notificacoes_eventos()
    
    return render(request, "core/dashboard.html", context)

@login_required
def busca_global(request):
    """
    View para busca global no sistema, retornando resultados de várias entidades.
    """
    query = request.GET.get('q', '')
    resultados = {}
    
    if query and len(query) >= 3:  # Exigir pelo menos 3 caracteres para busca
        # Busca em Alunos
        resultados['alunos'] = Aluno.objects.filter(
            Q(nome_completo__icontains=query) |
            Q(cpf__icontains=query) |
            Q(email__icontains=query)
        ).order_by('nome_completo')[:10]  # Limitar a 10 resultados
        
        # Busca em Professores
        resultados['professores'] = Professor.objects.filter(
            Q(nome__icontains=query) |
            Q(email__icontains=query) |
            Q(disciplinas__nome__icontains=query)  # Aqui está a correção
        ).distinct().order_by('nome')[:10]  # distinct() para evitar duplicatas
        
        # Busca em Turmas
        resultados['turmas'] = Turma.objects.filter(
            Q(nome__icontains=query) |
            Q(serie__icontains=query) |
            Q(turma_letra__icontains=query) |
            Q(periodo__icontains=query)
        ).order_by('nome')[:10]
        
        # Busca em Documentos
        resultados['documentos'] = Documento.objects.filter(
            Q(conteudo__icontains=query) |
            Q(aluno__nome_completo__icontains=query)
        ).order_by('-data_emissao')[:10]
        
        # Busca em Eventos
        resultados['eventos'] = Evento.objects.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query)
        ).order_by('data_inicio')[:10]
        
        # Busca em Matrículas (pelo nome do aluno)
        resultados['matriculas'] = Matricula.objects.filter(
            aluno__nome_completo__icontains=query
        ).order_by('-data_matricula')[:10]
    
    return render(request, 'core/busca_global.html', {
        'query': query,
        'resultados': resultados,
        'tem_resultados': any(resultados.values()) if resultados else False
    })
