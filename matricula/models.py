from django.db import models
from aluno.models import Aluno
from turma.models import Turma
from professor.models import Professor

class Matricula(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado'),
        ('transferido', 'Transferido')
    ]

    # Campos da Matrícula
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_matricula = models.DateField()
    ano_letivo = models.IntegerField()
    turma = models.ForeignKey('turma.Turma', on_delete=models.CASCADE)  # Referência à classe Turma no app turma
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.aluno.nome_completo} - {self.turma.nome} - Status: {self.status}"

