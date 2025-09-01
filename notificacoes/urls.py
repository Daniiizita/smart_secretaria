from django.urls import path
from . import views

app_name = 'notificacoes'

urlpatterns = [
    path('', views.lista_notificacoes, name='lista_notificacoes'),
    path('<int:notificacao_id>/ler/', views.marcar_como_lida, name='marcar_como_lida'),
    path('verificar/', views.verificar_novas_notificacoes, name='verificar_novas_notificacoes'),
]