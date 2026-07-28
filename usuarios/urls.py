from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('criar/', views.criar_usuario, name='criar_usuario'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
    path('<int:user_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:user_id>/excluir/', views.excluir_usuario, name='excluir_usuario'),
]