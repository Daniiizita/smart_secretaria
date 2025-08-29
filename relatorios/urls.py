from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('alunos-por-turma/excel/', views.alunos_por_turma_excel, name='alunos_por_turma_excel'),
    path('alunos-da-turma/<int:turma_id>/excel/', views.alunos_da_turma_excel, name='alunos_da_turma_excel'),
]