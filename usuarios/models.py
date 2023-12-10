from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TIPOS_USUARIO = [
    ('admin', 'Administrador'),
    ('secretario', 'Secretário'),
    ('professor', 'Professor'),
    ('aluno', 'Aluno'),
    ('responsavel', 'Responsável'),
    # Adicione outros tipos conforme necessário
]

    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO)

    # Adicione os campos related_name para evitar conflitos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='customuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='customuser_set',
        related_query_name='user',
    )

