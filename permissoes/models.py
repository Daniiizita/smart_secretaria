from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

User = get_user_model()

class PerfilAcesso(models.Model):
    TIPOS = [
        ('admin', 'Administrador'),
        ('secretaria', 'Secretaria'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        ('responsavel', 'Responsável')
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descricao = models.TextField(blank=True)
    grupo = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='perfil_acesso')
    
    class Meta:
        verbose_name = "Perfil de Acesso"
        verbose_name_plural = "Perfis de Acesso"
    
    def __str__(self):
        return self.nome

class TentativaLogin(models.Model):
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    sucesso = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tentativa de Login"
        verbose_name_plural = "Tentativas de Login"
        ordering = ['-timestamp']
    
    def __str__(self):
        status = "Sucesso" if self.sucesso else "Falha"
        return f"{self.username} - {status} - {self.timestamp}"
