from rest_framework import serializers
from ..models import Notificacao # troque "Aluno" pelo modelo do app

class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = '__all__'  # ou liste explicitamente os campos
