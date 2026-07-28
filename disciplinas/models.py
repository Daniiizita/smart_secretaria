from django.db import models

# Create your models here.
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    carga_horaria = models.IntegerField(default=0)
    ativa = models.BooleanField(default=True)
    
    # Campos para tornar mais escalável
    nivel_ensino = models.CharField(max_length=20, blank=True, null=True,
                                   choices=[
                                       ('EI', 'Educação Infantil'),
                                       ('EFI', 'Ensino Fundamental I'),
                                       ('EFII', 'Ensino Fundamental II'),
                                       ('EM', 'Ensino Médio'),
                                   ])
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
        
    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ['nome']
