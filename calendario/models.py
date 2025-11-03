from django.db import models

class Evento(models.Model):
    TIPO_CHOICES = [
        ('feriado', 'Feriado'),
        ('evento_escolar', 'Evento Escolar'),
        ('reuniao', 'Reunião'),
        ('outro', 'Outro'),
    ]

    # Campos do Evento
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.titulo} - Tipo: {self.tipo}"
