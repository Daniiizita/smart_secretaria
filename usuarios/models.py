from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    TIPOS_USUARIO = (
        ('admin', 'Administrador'),
        ('diretor', 'Diretor'),
        ('secretario', 'Secretário'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        ('responsavel', 'Responsável'),
    )
    
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='admin')
    
    # Evita conflito de nomes com o modelo User do Django
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    
    def __str__(self):
        return self.username

class ConviteRegistro(models.Model):
    aluno = models.ForeignKey('aluno.Aluno', on_delete=models.CASCADE, related_name='convites')
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    expira_em = models.DateTimeField()
    usado = models.BooleanField(default=False)
    criado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='convites_criados')

    def __str__(self):
        return f"Convite para {self.aluno.nome_completo}"
    
    @classmethod
    def gerar_convite(cls, aluno, email, criado_por, dias_validade=7):
        """Gera um novo convite de registro para um aluno"""
        token = get_random_string(64)
        expira_em = timezone.now() + timedelta(days=dias_validade)
        
        return cls.objects.create(
            aluno=aluno,
            email=email,
            token=token,
            expira_em=expira_em,
            criado_por=criado_por
        )
    
    def esta_valido(self):
        """Verifica se o convite ainda é válido"""
        return not self.usado and timezone.now() <= self.expira_em

