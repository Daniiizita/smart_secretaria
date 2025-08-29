from django.db import models
from professor.models import Professor

# Constantes para escolha de nível e série
NIVEL_CHOICES = [
    ('EI', 'Educação Infantil'),
    ('EFI', 'Ensino Fundamental I'),
    ('EFII', 'Ensino Fundamental II'),
    ('EM', 'Ensino Médio'),
]

SERIE_CHOICES = [
    (1, '1º Período - Educação Infantil'),
    (2, '2º Período - Educação Infantil'),
    (3, '1º Ano - Ensino Fundamental I'),
    (4, '2º Ano - Ensino Fundamental I'),
    (5, '3º Ano - Ensino Fundamental I'),
    (6, '4º Ano - Ensino Fundamental I'),
    (7, '5º Ano - Ensino Fundamental I'),
    (8, '6º Ano - Ensino Fundamental II'),
    (9, '7º Ano - Ensino Fundamental II'),
    (10, '8º Ano - Ensino Fundamental II'),
    (11, '9º Ano - Ensino Fundamental II'),
    (12, '1º Ano - Ensino Médio'),
    (13, '2º Ano - Ensino Médio'),
    (14, '3º Ano - Ensino Médio'),
]

TURMA_LETRA_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
]

PERIODO_CHOICES = [
    ('Manhã', 'Manhã'),
    ('Tarde', 'Tarde'),
    ('Noite', 'Noite'),
    ('Integral', 'Integral'),
]


class Turma(models.Model):
    serie = models.IntegerField(choices=SERIE_CHOICES)
    turma_letra = models.CharField(max_length=2, choices=TURMA_LETRA_CHOICES, default="A")
    professor_responsavel = models.ForeignKey(Professor, on_delete=models.CASCADE)
    horario_aulas = models.CharField(max_length=100, blank=True, null=True)
    ano = models.IntegerField(default=2023)
    periodo = models.CharField(max_length=20, choices=PERIODO_CHOICES, default="Manhã")
    nome = models.CharField(max_length=100, blank=True)
    nivel_ensino_sigla = models.CharField(max_length=10, choices=NIVEL_CHOICES, blank=True)

    def save(self, *args, **kwargs):
        """
        Sempre que salvar, monta o nome padronizado e define o nível
        """
        # Obter o texto da série a partir das escolhas
        serie_texto = dict(SERIE_CHOICES).get(self.serie, f"{self.serie}º Ano")
        
        # Dividir o texto para separar o ano escolar do nível de ensino
        partes = serie_texto.split(' - ')
        
        if len(partes) > 1:
            ano_escolar = partes[0]  # Ex: "1º Ano"
            nivel_ensino_texto = partes[1]  # Ex: "Ensino Fundamental I"
            
            # Montar o nome da turma com o novo formato
            self.nome = f"{ano_escolar} {self.turma_letra} - {nivel_ensino_texto} - {self.periodo} - {self.ano}"
        else:
            # Caso não tenha o separador " - ", usar o formato antigo
            self.nome = f"{serie_texto} {self.turma_letra} - {self.periodo} - {self.ano}"
        
        # Definir a sigla do nível com base na série
        if 1 <= self.serie <= 2:
            self.nivel_ensino_sigla = 'EI'
        elif 3 <= self.serie <= 7:
            self.nivel_ensino_sigla = 'EFI'
        elif 8 <= self.serie <= 11:
            self.nivel_ensino_sigla = 'EFII'
        elif 12 <= self.serie <= 14:
            self.nivel_ensino_sigla = 'EM'
        else:
            self.nivel_ensino_sigla = 'ND'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

