from .models import LogAtividade
from django.utils import timezone

def registrar_atividade(usuario, acao, descricao_detalhada=None):
    """
    Registra uma atividade no sistema de logs.
    
    Parâmetros:
    - usuario: Instância de CustomUser que realizou a ação
    - acao: String descrevendo a ação realizada (ex: "Criação de Aluno")
    - descricao_detalhada: Detalhes adicionais sobre a ação (opcional)
    
    Retorna:
    - Instância do LogAtividade criado
    """
    return LogAtividade.objects.create(
        usuario=usuario,
        acao=acao,
        descricao_detalhada=descricao_detalhada,
        data_hora=timezone.now()
    )