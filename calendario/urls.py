from django.urls import path
from . import views

app_name = 'calendario'

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('mensal/', views.calendario_mensal, name='calendario_mensal'),
    path('evento/<int:pk>/', views.detalhe_evento, name='detalhe_evento'),
    path('evento/novo/', views.novo_evento, name='novo_evento'),
    path('evento/<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('evento/<int:pk>/excluir/', views.excluir_evento, name='excluir_evento'),
]