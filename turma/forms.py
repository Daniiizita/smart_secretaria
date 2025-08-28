from django import forms
from .models import Turma

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['serie', 'turma_letra', 'professor_responsavel', 'horario_aulas', 'ano', 'periodo']
        widgets = {
            'horario_aulas': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super(TurmaForm, self).__init__(*args, **kwargs)
        self.fields['serie'].widget.attrs.update({'class': 'form-control'})
        self.fields['turma_letra'].widget.attrs.update({'class': 'form-control'})
        self.fields['professor_responsavel'].widget.attrs.update({'class': 'form-control'})
        self.fields['horario_aulas'].widget.attrs.update({'class': 'form-control'})
        self.fields['ano'].widget.attrs.update({'class': 'form-control'})
        self.fields['periodo'].widget.attrs.update({'class': 'form-control'})