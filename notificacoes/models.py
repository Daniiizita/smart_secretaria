from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notificacao(models.Model):
    TIPOS = (
        ('evento', 'Evento Próximo'),
        ('documento', 'Documento Importante'),
        ('matricula', 'Matrícula Pendente'),
        ('sistema', 'Sistema'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    link = models.CharField(max_length=200, blank=True, null=True)
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-criada_em']
        
    def __str__(self):
        return self.titulo
