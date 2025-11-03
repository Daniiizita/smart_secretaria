from django.urls import path
from . import views

app_name = 'aluno'

urlpatterns = [
    path('', views.lista_alunos, name='lista_alunos'),
    path('novo/', views.novo_aluno, name='novo_aluno'),
    path('<int:aluno_id>/', views.detalhe_aluno, name='detalhe_aluno'),
    path('<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),
]
