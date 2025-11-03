from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome_completo', 'data_nascimento', 'nome_pai', 'nome_mae', 
                 'cpf', 'rg', 'endereco', 'telefone_contato', 'email', 
                 'nome_responsavel', 'turma', 'foto']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos')
        return cpf