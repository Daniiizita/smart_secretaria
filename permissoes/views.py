from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from datetime import timedelta
from .models import TentativaLogin

@login_required
@permission_required('permissoes.view_tentativalogin')
def monitoramento_login(request):
    # Definir períodos para análise
    hoje = timezone.now().date()
    ontem = hoje - timedelta(days=1)
    ultimos_7_dias = hoje - timedelta(days=7)
    ultimos_30_dias = hoje - timedelta(days=30)
    
    # Buscar estatísticas
    estatisticas = {
        'hoje': {
            'total': TentativaLogin.objects.filter(timestamp__date=hoje).count(),
            'sucesso': TentativaLogin.objects.filter(timestamp__date=hoje, sucesso=True).count(),
            'falha': TentativaLogin.objects.filter(timestamp__date=hoje, sucesso=False).count()
        },
        'ontem': {
            'total': TentativaLogin.objects.filter(timestamp__date=ontem).count(),
            'sucesso': TentativaLogin.objects.filter(timestamp__date=ontem, sucesso=True).count(),
            'falha': TentativaLogin.objects.filter(timestamp__date=ontem, sucesso=False).count()
        },
        'ultimos_7_dias': {
            'total': TentativaLogin.objects.filter(timestamp__date__gte=ultimos_7_dias).count(),
            'sucesso': TentativaLogin.objects.filter(timestamp__date__gte=ultimos_7_dias, sucesso=True).count(),
            'falha': TentativaLogin.objects.filter(timestamp__date__gte=ultimos_7_dias, sucesso=False).count()
        },
        'ultimos_30_dias': {
            'total': TentativaLogin.objects.filter(timestamp__date__gte=ultimos_30_dias).count(),
            'sucesso': TentativaLogin.objects.filter(timestamp__date__gte=ultimos_30_dias, sucesso=True).count(),
            'falha': TentativaLogin.objects.filter(timestamp__date__gte=ultimos_30_dias, sucesso=False).count()
        }
    }
    
    # Últimas tentativas de login
    ultimas_tentativas = TentativaLogin.objects.all().order_by('-timestamp')[:100]
    
    return render(request, 'permissoes/monitoramento_login.html', {
        'estatisticas': estatisticas,
        'ultimas_tentativas': ultimas_tentativas
    })
