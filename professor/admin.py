from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone_contato', 'data_admissao')
    search_fields = ('nome', 'email')
    filter_horizontal = ('disciplinas',)  # Mantém a relação com disciplinas
