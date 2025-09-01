from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from .models import Notificacao
from .services import verificar_eventos_proximos, verificar_matriculas_pendentes, verificar_documentos_importantes

@login_required
def lista_notificacoes(request):
    """
    Exibe todas as notificações do usuário logado
    """
    notificacoes = Notificacao.objects.filter(usuario=request.user)
    
    return render(request, 'notificacoes/lista_notificacoes.html', {
        'notificacoes': notificacoes,
    })

@login_required
@require_POST
def marcar_como_lida(request, notificacao_id):
    """
    Marca uma notificação como lida
    """
    try:
        notificacao = Notificacao.objects.get(id=notificacao_id, usuario=request.user)
        notificacao.lida = True
        notificacao.save()
    except Notificacao.DoesNotExist:
        pass
    return redirect('notificacoes:lista_notificacoes')

@login_required
def verificar_novas_notificacoes(request):
    """
    Endpoint para verificar novas notificações via AJAX
    """
    # Executa verificação de eventos, matrículas e documentos
    verificar_eventos_proximos()
    verificar_matriculas_pendentes()
    verificar_documentos_importantes()
    
    count = Notificacao.objects.filter(usuario=request.user, lida=False).count()
    
    return JsonResponse({
        'count': count,
        'status': 'success'
    })
