from django.urls import path
from . import views

app_name = 'aluno'

urlpatterns = [
    path('', views.lista_alunos, name='lista_alunos'),
    path('novo/', views.novo_aluno, name='novo_aluno'),
    path('<int:aluno_id>/', views.detalhe_aluno, name='detalhe_aluno'),
    path('<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),
    path('<int:aluno_id>/convite/', views.gerar_convite_aluno, name='gerar_convite'),
    path('convites/', views.listar_convites, name='listar_convites'),
]

urlpatterns += [
    path('registro/convite/<str:token>/', views.registrar_com_convite, name='registrar_com_convite'),
]
