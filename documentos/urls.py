from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    path('', views.lista_documentos, name='lista_documentos'),
    path('novo/', views.novo_documento, name='novo_documento'),
    path('<int:documento_id>/', views.detalhe_documento, name='detalhe_documento'),
    path('<int:documento_id>/editar/', views.editar_documento, name='editar_documento'),
    path('<int:documento_id>/excluir/', views.excluir_documento, name='excluir_documento'),
    path('<int:documento_id>/imprimir/', views.imprimir_documento, name='imprimir_documento'),
]