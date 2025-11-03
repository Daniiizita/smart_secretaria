def notificacoes_nao_lidas(request):
    """
    Adiciona o contador de notificações não lidas ao contexto de todos os templates.
    """
    contador = 0
    if hasattr(request, 'user') and request.user.is_authenticated:
        contador = request.user.notificacao_set.filter(lida=False).count()
    return {'notificacoes_nao_lidas': contador}