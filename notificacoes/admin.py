from django.contrib import admin
from .models import Notificacao

class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'tipo', 'lida', 'criada_em']
    list_filter = ['lida', 'tipo', 'criada_em']
    search_fields = ['titulo', 'mensagem', 'usuario__username']
    date_hierarchy = 'criada_em'
    
admin.site.register(Notificacao, NotificacaoAdmin)
