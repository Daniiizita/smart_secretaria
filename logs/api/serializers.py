from rest_framework import serializers
from ..models import LogAtividade  # troque "Aluno" pelo modelo do app

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAtividade
        fields = '__all__'  # ou liste explicitamente os campos
