from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

def associar_usuario_ao_grupo(usuario, tipo_usuario):
    """
    Associa um usuário a um grupo baseado no seu tipo.
    
    Args:
        usuario: Instância do modelo de usuário
        tipo_usuario: String com o tipo de usuário ('admin', 'secretaria', 'professor', 'aluno', 'responsavel')
    
    Returns:
        True se a associação foi bem-sucedida, False caso contrário
    """
    mapeamento_grupos = {
        'admin': 'Administrador',
        'administrador': 'Administrador',
        'secretaria': 'Secretaria',
        'professor': 'Professor',
        'aluno': 'Aluno',
        'responsavel': 'Responsavel'
    }
    
    tipo_normalizado = tipo_usuario.lower()
    nome_grupo = mapeamento_grupos.get(tipo_normalizado)
    
    if not nome_grupo:
        return False
    
    try:
        grupo = Group.objects.get(name=nome_grupo)
        usuario.groups.clear()  # Remove de todos os grupos anteriores
        usuario.groups.add(grupo)
        return True
    except Group.DoesNotExist:
        return False