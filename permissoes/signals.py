from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .models import TentativaLogin

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def login_bem_sucedido(sender, request, user, **kwargs):
    """Registra tentativas de login bem-sucedidas"""
    TentativaLogin.objects.create(
        username=user.username,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        sucesso=True
    )

@receiver(user_login_failed)
def login_falhou(sender, credentials, request, **kwargs):
    """Registra tentativas de login malsucedidas"""
    if request:
        TentativaLogin.objects.create(
            username=credentials.get('username', ''),
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            sucesso=False
        )