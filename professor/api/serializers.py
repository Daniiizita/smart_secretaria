from rest_framework import serializers
from ..models import Professor  # troque "Aluno" pelo modelo do app

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'  # ou liste explicitamente os campos
