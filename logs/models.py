from django.db import models
from django.contrib.auth.models import User

class LogAtividade(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acao = models.CharField(max_length=50)
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao_detalhada = models.TextField()

    def __str__(self):
        return f"{self.usuario.username} - {self.acao}"

#Pretendo automatizar o log de atividades do sistema no futuro
# Create your models here.
