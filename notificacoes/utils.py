from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from calendario.models import Evento
from matricula.models import Matricula
from .models import Notificacao

User = get_user_model()

def criar_notificacoes_eventos():
    """Cria notificações para eventos próximos (próximos 3 dias)"""
    hoje = datetime.now()
    limite = hoje + timedelta(days=3)
    
    # Encontrar eventos próximos
    eventos_proximos = Evento.objects.filter(
        data_inicio__gte=hoje,
        data_inicio__lte=limite
    )
    
    # Encontrar usuários que devem ser notificados (todos os administradores neste exemplo)
    usuarios = User.objects.filter(is_staff=True)
    
    # Criar notificações
    for evento in eventos_proximos:
        for usuario in usuarios:
            # Verificar se já existe notificação para este evento e usuário
            notificacao_existente = Notificacao.objects.filter(
                usuario=usuario,
                tipo='evento',
                titulo=f"Evento próximo: {evento.titulo}",
                link=f"/calendario/evento/{evento.id}/"
            ).exists()
            
            if not notificacao_existente:
                Notificacao.objects.create(
                    usuario=usuario,
                    tipo='evento',
                    titulo=f"Evento próximo: {evento.titulo}",
                    mensagem=f"O evento {evento.titulo} está agendado para {evento.data_inicio.strftime('%d/%m/%Y')}",
                    link=f"/calendario/evento/{evento.id}/"
                )