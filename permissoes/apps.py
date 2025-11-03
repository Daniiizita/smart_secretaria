from django.apps import AppConfig


class PermissoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'permissoes'
    
    def ready(self):
        import permissoes.signals  # Importar sinais quando o app for carregado
