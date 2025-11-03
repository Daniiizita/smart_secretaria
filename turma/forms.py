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
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})