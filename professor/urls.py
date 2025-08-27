from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    path('', views.lista_professores, name='lista_professores'),
    path('novo/', views.novo_professor, name='novo_professor'),
    path('<int:professor_id>/', views.detalhe_professor, name='detalhe_professor'),
    path('<int:professor_id>/editar/', views.editar_professor, name='editar_professor'),
    path('<int:professor_id>/excluir/', views.excluir_professor, name='excluir_professor'),
]
