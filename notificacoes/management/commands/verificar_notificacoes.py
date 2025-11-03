from django.core.management.base import BaseCommand
from notificacoes.services import (
    verificar_eventos_proximos,
    verificar_matriculas_pendentes,
    verificar_documentos_importantes
)

class Command(BaseCommand):
    help = 'Verifica e gera notificações para eventos próximos e matrículas pendentes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Verificando eventos próximos...')
        verificar_eventos_proximos()
        
        self.stdout.write('Verificando matrículas pendentes...')
        verificar_matriculas_pendentes()
        
        self.stdout.write('Verificando documentos importantes...')
        verificar_documentos_importantes()
        
        self.stdout.write(self.style.SUCCESS('Verificação de notificações concluída com sucesso!'))