from django.contrib import admin
from .models import Disciplina

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'carga_horaria', 'nivel_ensino', 'ativa')
    search_fields = ('nome', 'codigo')
    list_filter = ('nivel_ensino', 'ativa')
