from django.conf import settings
from django.db import models

class LogAtividade(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="logs"
    )
    acao = models.CharField(max_length=50)
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao_detalhada = models.TextField()

    def __str__(self):
        return f"{self.usuario} - {self.acao}"
