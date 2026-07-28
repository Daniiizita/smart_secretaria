from django.urls import path, include
from . import views

app_name = 'disciplinas'

urlpatterns = [
    path('', views.lista_disciplinas, name='lista_disciplinas'),
    path('nova/', views.nova_disciplina, name='nova_disciplina'),
    path('<int:disciplina_id>/', views.detalhe_disciplina, name='detalhe_disciplina'),
    path('<int:disciplina_id>/editar/', views.editar_disciplina, name='editar_disciplina'),
    path('<int:disciplina_id>/excluir/', views.excluir_disciplina, name='excluir_disciplina'),
]