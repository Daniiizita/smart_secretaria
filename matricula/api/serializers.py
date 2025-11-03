from rest_framework import serializers
from ..models import Matricula  # troque "Aluno" pelo modelo do app

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'  # ou liste explicitamente os campos
