from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Evento

User = get_user_model()

class EventoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            tipo='admin'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.evento = Evento.objects.create(
            titulo='Reunião de Pais',
            descricao='Reunião semestral com os pais',
            data_inicio='2023-07-15T14:00:00Z',
            data_fim='2023-07-15T16:00:00Z',
            tipo='reuniao'
        )
        
    def test_lista_eventos_view(self):
        response = self.client.get(reverse('calendario:lista_eventos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reunião de Pais')
        
    def test_detalhe_evento_view(self):
        response = self.client.get(reverse('calendario:detalhe_evento', args=[self.evento.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reunião semestral com os pais')
