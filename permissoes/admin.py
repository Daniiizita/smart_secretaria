from django.contrib import admin
from .models import PerfilAcesso, TentativaLogin

@admin.register(PerfilAcesso)
class PerfilAcessoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'grupo']
    list_filter = ['tipo']
    search_fields = ['nome', 'descricao']

@admin.register(TentativaLogin)
class TentativaLoginAdmin(admin.ModelAdmin):
    list_display = ['username', 'sucesso', 'ip_address', 'timestamp']
    list_filter = ['sucesso', 'timestamp']
    search_fields = ['username', 'ip_address']
    date_hierarchy = 'timestamp'
