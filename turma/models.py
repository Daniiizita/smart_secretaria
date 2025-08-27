from django.db import models
from professor.models import Professor


class Turma(models.Model):
    serie = models.IntegerField()
    turma_letra = models.CharField(max_length=2, default="A")
    professor_responsavel = models.ForeignKey(Professor, on_delete=models.CASCADE)
    horario_aulas = models.CharField(max_length=100, blank=True, null=True)
    ano = models.IntegerField(default=2023)
    periodo = models.CharField(max_length=20, default="Manhã")
    nome = models.CharField(max_length=100, blank=True)  # Adicionado explicitamente

    def save(self, *args, **kwargs):
        """
        Sempre que salvar, monta o nome padronizado
        incluindo o ano (importante pro seu caso).
        """
        print(f"DEBUG - Salvando turma: serie={self.serie}, letra={self.turma_letra}, ano={self.ano}, periodo={self.periodo}")
        self.nome = f"{self.serie}º Ano {self.turma_letra} - {self.periodo} {self.ano}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

