from rest_framework import serializers
from aluno.models import Aluno
from professor.models import Professor
from turma.models import Turma
from calendario.models import Evento
from matricula.models import Matricula
from documentos.models import Documento

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nome_completo', 'data_nascimento', 'email', 'telefone_contato', 'turma']
        # Use fields = '__all__' para incluir todos os campos


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'nome', 'cpf', 'rg', 'endereco','telefone_contato', 'email', 'data_admissao', 'disciplinas', 'turma']


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'