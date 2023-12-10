from django.db import models

class Professor(models.Model):
    # Campos obrigatórios
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=200)
    telefone_contato = models.CharField(max_length=20)
    email = models.EmailField()
    data_admissao = models.DateField()

    # Relação com Disciplinas
    disciplinas = models.ManyToManyField('Disciplina', blank=True)

    # Campo opcional
    foto = models.ImageField(upload_to='professores/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
