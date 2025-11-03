from django import forms
from .models import Professor, Disciplina

class ProfessorForm(forms.ModelForm):
    # Adiciona um campo MultipleChoiceField para disciplinas
    disciplinas = forms.ModelMultipleChoiceField(
        queryset=Disciplina.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Disciplinas'
    )

    
    class Meta:
        model = Professor
        fields = [
            'nome', 'cpf', 'rg', 'orgao_expedidor', 
            'data_nascimento', 'endereco', 'telefone_contato',
            'email', 'data_admissao', 'naturalidade',
            'disciplinas', 'foto'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter somente 11 dígitos, sem "()" ou "." ')
        return cpf
    
    def clean_rg(self):
        rg = self.cleaned_data.get('rg')
        if rg and len(rg) != 7:
            raise forms.ValidationError('RG deve conter somente 7 dígitos, sem "-" ou "." ')
        return rg

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome']
        
class CheckboxList(forms.CheckboxSelectMultiple):
    template_name = 'widgets/checkbox_list.html'