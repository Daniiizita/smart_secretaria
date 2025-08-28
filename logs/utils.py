from django.utils import timezone
from .models import LogAtividade

def registrar_atividade(usuario, acao, descricao_detalhada=None):
    """
    Registra uma atividade realizada por um usuário no sistema.
    
    Args:
        usuario: O usuário que realizou a ação
        acao: Descrição curta da ação (ex: "Criação de Aluno")
        descricao_detalhada: Descrição mais detalhada da ação (opcional)
    """
    try:
        # Verifica se o usuário é válido
        if usuario and hasattr(usuario, 'id'):
            LogAtividade.objects.create(
                usuario=usuario,
                data_hora=timezone.now(),
                acao=acao,
                descricao_detalhada=descricao_detalhada or ""
            )
        else:
            print("Aviso: Tentativa de registrar log sem usuário válido")
    except Exception as e:
        print(f"Erro ao registrar atividade: {str(e)}")
        # Não propaga a exceção, apenas registra o erro