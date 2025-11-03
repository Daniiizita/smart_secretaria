from rest_framework import serializers
from ..models import Turma  # troque "Aluno" pelo modelo do app

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'  # ou liste explicitamente os campos
