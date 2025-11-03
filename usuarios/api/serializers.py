from rest_framework import serializers
from ..models import CustomUser  # troque "Aluno" pelo modelo do app

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  # ou liste explicitamente os campos
