from django import forms
from .models import Professor, Disciplina

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'cpf', 'rg', 'endereco', 'telefone_contato', 
                 'email', 'data_admissao', 'disciplinas', 'foto']
        widgets = {
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos')
        return cpf

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome']