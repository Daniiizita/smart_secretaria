from django.urls import path
from . import views

app_name = 'matricula'

urlpatterns = [
    path('', views.lista_matriculas, name='lista_matriculas'),
    path('nova/', views.nova_matricula, name='nova_matricula'),
    path('<int:matricula_id>/', views.detalhe_matricula, name='detalhe_matricula'),
    path('<int:matricula_id>/editar/', views.editar_matricula, name='editar_matricula'),
    path('<int:matricula_id>/excluir/', views.excluir_matricula, name='excluir_matricula'),
    path('<int:matricula_id>/status/<str:novo_status>/', views.mudar_status_matricula, name='mudar_status_matricula'),
]