from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descricao', 'data_inicio', 'data_fim', 'tipo']
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajusta os campos datetime para exibição correta no formato HTML datetime-local
        if self.instance.pk:
            if self.instance.data_inicio:
                self.initial['data_inicio'] = self.instance.data_inicio.strftime('%Y-%m-%dT%H:%M')
            if self.instance.data_fim:
                self.initial['data_fim'] = self.instance.data_fim.strftime('%Y-%m-%dT%H:%M')