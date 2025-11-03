from rest_framework import serializers
from ..models import Documento  # troque "Aluno" pelo modelo do app

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'  # ou liste explicitamente os campos
