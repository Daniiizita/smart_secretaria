from django import forms
from .models import Professor
from disciplinas.models import Disciplina  # Atualizado o import

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'cpf', 'rg', 'endereco', 'telefone_contato', 
                 'email', 'data_admissao', 'disciplinas', 'foto']
        widgets = {
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ProfessorForm, self).__init__(*args, **kwargs)
        # Podemos ordenar as disciplinas ou aplicar filtros adicionais se necessário
        self.fields['disciplinas'].queryset = Disciplina.objects.filter(ativa=True).order_by('nome')
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos')
        return cpf

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome']