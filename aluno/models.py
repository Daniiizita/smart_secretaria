from django.db import models
from professor.models import Professor
from turma.models import Turma
    

class Aluno(models.Model):
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    nome_pai = models.CharField(max_length=100, blank=True, null=True)
    nome_mae = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=200)
    telefone_contato = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True, null=True)
    nome_responsavel = models.CharField(max_length=100, blank=True, null=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='alunos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome_completo} - Turma: {self.turma}"




