from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import Notificacao
from calendario.models import Evento
from matricula.models import Matricula
from documentos.models import Documento

def criar_notificacao(usuario, titulo, mensagem, tipo, prioridade='normal', objeto_relacionado=None, url_destino=''):
    """
    Cria uma nova notificação para um usuário
    """
    content_type = None
    object_id = None
    
    if objeto_relacionado:
        content_type = ContentType.objects.get_for_model(objeto_relacionado.__class__)
        object_id = objeto_relacionado.id
    
    notificacao = Notificacao.objects.create(
        usuario=usuario,
        titulo=titulo,
        mensagem=mensagem,
        tipo=tipo,
        prioridade=prioridade,
        content_type=content_type,
        object_id=object_id,
        url_destino=url_destino
    )
    
    return notificacao

def verificar_eventos_proximos():
    """
    Verifica eventos que ocorrerão nos próximos dias e gera notificações
    """
    hoje = datetime.now().date()
    em_tres_dias = hoje + timedelta(days=3)
    
    eventos_proximos = Evento.objects.filter(
        data__gte=hoje,
        data__lte=em_tres_dias
    )
    
    for evento in eventos_proximos:
        # Verifica se já existe uma notificação para este evento
        if not Notificacao.objects.filter(
            content_type=ContentType.objects.get_for_model(Evento),
            object_id=evento.id,
            tipo='evento'
        ).exists():
            # Para cada usuário administrativo, cria uma notificação
            from django.contrib.auth import get_user_model
            User = get_user_model()
            for usuario in User.objects.filter(is_staff=True):
                dias_restantes = (evento.data - hoje).days
                if dias_restantes == 0:
                    mensagem = f"O evento '{evento.titulo}' acontecerá hoje!"
                    prioridade = 'alta'
                elif dias_restantes == 1:
                    mensagem = f"O evento '{evento.titulo}' acontecerá amanhã!"
                    prioridade = 'alta'
                else:
                    mensagem = f"O evento '{evento.titulo}' acontecerá em {dias_restantes} dias."
                    prioridade = 'normal'
                    
                criar_notificacao(
                    usuario=usuario,
                    titulo=f"Evento Próximo: {evento.titulo}",
                    mensagem=mensagem,
                    tipo='evento',
                    prioridade=prioridade,
                    objeto_relacionado=evento,
                    url_destino=reverse('calendario:detalhe_evento', args=[evento.id])
                )

def verificar_matriculas_pendentes():
    """
    Verifica matrículas com status pendente e gera notificações
    """
    # Matrículas com status pendente há mais de 7 dias
    data_limite = datetime.now() - timedelta(days=7)
    
    matriculas_pendentes = Matricula.objects.filter(
        status='pendente',
        data_matricula__lte=data_limite
    )
    
    for matricula in matriculas_pendentes:
        # Verifica se já existe uma notificação para esta matrícula nos últimos 7 dias
        if not Notificacao.objects.filter(
            content_type=ContentType.objects.get_for_model(Matricula),
            object_id=matricula.id,
            tipo='matricula',
            data_criacao__gte=datetime.now() - timedelta(days=7)
        ).exists():
            # Para cada usuário administrativo, cria uma notificação
            from django.contrib.auth import get_user_model
            User = get_user_model()
            for usuario in User.objects.filter(is_staff=True):
                criar_notificacao(
                    usuario=usuario,
                    titulo=f"Matrícula Pendente: {matricula.aluno.nome_completo}",
                    mensagem=f"A matrícula do aluno {matricula.aluno.nome_completo} está pendente há mais de 7 dias e precisa ser revisada.",
                    tipo='matricula',
                    prioridade='alta',
                    objeto_relacionado=matricula,
                    url_destino=reverse('matricula:detalhe_matricula', args=[matricula.id])
                )

def verificar_documentos_importantes():
    """
    Verifica documentos importantes que precisam de atenção
    """
    # Exemplo: documentos com alguma flag de "importante" ou pendentes de revisão
    documentos_importantes = Documento.objects.filter(
        importante=True,  # Assumindo que existe este campo
        revisado=False    # Assumindo que existe este campo
    )
    
    for documento in documentos_importantes:
        # Verifica se já existe uma notificação para este documento nos últimos 7 dias
        if not Notificacao.objects.filter(
            content_type=ContentType.objects.get_for_model(Documento),
            object_id=documento.id,
            tipo='documento',
            data_criacao__gte=datetime.now() - timedelta(days=7)
        ).exists():
            # Para cada usuário administrativo, cria uma notificação
            from django.contrib.auth import get_user_model
            User = get_user_model()
            for usuario in User.objects.filter(is_staff=True):
                criar_notificacao(
                    usuario=usuario,
                    titulo=f"Documento Importante: {documento.titulo}",
                    mensagem=f"O documento {documento.titulo} está marcado como importante e precisa ser revisado.",
                    tipo='documento',
                    prioridade='alta',
                    objeto_relacionado=documento,
                    url_destino=reverse('documentos:detalhe_documento', args=[documento.id])
                )