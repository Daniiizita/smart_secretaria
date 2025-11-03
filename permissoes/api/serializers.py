from rest_framework import serializers
from ..models import PerfilAcesso, TentativaLogin  # troque "Aluno" pelo modelo do app

class PerfilAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilAcesso
        fields = '__all__'  # ou liste explicitamente os campos
        
class TentativaLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = TentativaLogin
        fields = '__all__'  # ou liste explicitamente os campos
