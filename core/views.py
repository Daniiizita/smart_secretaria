#core.views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from aluno.models import Aluno
from professor.models import Professor
from calendario.models import Evento
from django.utils import timezone

#TODO incluir roteamento quando criar uma API

def index(request):
    """
    View da página inicial (FBV = Function-Based View).
    - 'request' é obrigatório para qualquer view.
    - Retorna HTML renderizando o template com um contexto.
    """
    context = {"title": "SmartSecretaria", "subtitle": "Home Page"} #Valores que serão chamados dinânicamente nos templates pelo jinja2
    return render(request, "core/index.html", context)

@login_required
def dashboard(request):
    # Contagens
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    
    # Próximos eventos
    hoje = timezone.now()
    proximos_eventos = Evento.objects.filter(
        data_inicio__gte=hoje
    ).order_by('data_inicio')[:5]
    
    # Últimos alunos cadastrados
    ultimos_alunos = Aluno.objects.all().order_by('-id')[:5]
    
    context = {
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'proximos_eventos': proximos_eventos,
        'ultimos_alunos': ultimos_alunos,
    }
    
    return render(request, "core/dashboard.html", context)
