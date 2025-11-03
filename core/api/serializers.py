
from rest_framework import serializers
from aluno.models import Aluno
from calendario.models import Evento
from logs.models import LogAtividade


class AlunoSimpleSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listas de alunos.
    """
    class Meta:
        model = Aluno
        fields = ['id', 'nome_completo', 'foto']


class EventoSimpleSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listas de eventos.
    """
    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'data_inicio']


class LogAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAtividade
        fields = ['id', 'acao', 'data_hora', 'usuario_username']