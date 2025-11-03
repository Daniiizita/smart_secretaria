# Exemplo de melhoria em core/api/urls.py
from django.urls import path
from .views import DashboardAPIView
 
urlpatterns = [
    # Uma URL mais descritiva.
    path('', DashboardAPIView.as_view(), name='dashboard-data'),
]
