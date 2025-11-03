from django.db import models
from usuarios.models import CustomUser

class LogAtividade(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='logs')
    data_hora = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=100)
    descricao_detalhada = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'Log de Atividade'
        verbose_name_plural = 'Logs de Atividades'

    def __str__(self):
        return f"{self.data_hora} - {self.usuario} - {self.acao}"
    
    @property
    def usuario_username(self):
        return self.usuario.username if self.usuario else 'Sistema'
