from django.urls import path
from . import views

app_name = 'permissoes'

urlpatterns = [
    path('monitoramento-login/', views.monitoramento_login, name='monitoramento_login'),
]