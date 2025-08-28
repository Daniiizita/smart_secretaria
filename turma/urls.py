from django.urls import path
from . import views

app_name = 'turma'

urlpatterns = [
    path('', views.lista_turmas, name='lista_turmas'),
    path('nova/', views.nova_turma, name='nova_turma'),
    path('<int:turma_id>/', views.detalhe_turma, name='detalhe_turma'),
    path('<int:turma_id>/editar/', views.editar_turma, name='editar_turma'),
    path('<int:turma_id>/excluir/', views.excluir_turma, name='excluir_turma'),
]
