from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('alunos-por-turma/excel/', views.alunos_por_turma_excel, name='alunos_por_turma_excel'),
    path('alunos-da-turma/<int:turma_id>/excel/', views.alunos_da_turma_excel, name='alunos_da_turma_excel'),
    path('alunos-por-turma/pdf/', views.alunos_por_turma_pdf, name='alunos_por_turma_pdf'),
    path('alunos-da-turma/<int:turma_id>/pdf/', views.alunos_da_turma_pdf, name='alunos_da_turma_pdf'),
]