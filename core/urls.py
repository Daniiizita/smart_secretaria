# core/urls.py

from django.urls import path
from . import views, api_views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('busca/', views.busca_global, name='busca_global'),
    path('api/busca-rapida/', api_views.busca_rapida_api, name='busca_rapida_api'),
]