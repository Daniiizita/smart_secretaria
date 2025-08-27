from .models import LogAtividade

def registrar_atividade(usuario, acao, descricao_detalhada):
    """
    Registra uma atividade no sistema.
    
    Args:
        usuario: Usuário que realizou a ação
        acao: Descrição curta da ação (max 50 caracteres)
        descricao_detalhada: Descrição completa da ação
    """
    LogAtividade.objects.create(
        usuario=usuario,
        acao=acao,
        descricao_detalhada=descricao_detalhada
    )
    return True