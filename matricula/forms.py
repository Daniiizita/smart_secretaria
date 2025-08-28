from django import forms
from .models import Matricula
from aluno.models import Aluno
from turma.models import Turma

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['aluno', 'turma', 'data_matricula', 'ano_letivo', 'status']
        widgets = {
            'data_matricula': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(MatriculaForm, self).__init__(*args, **kwargs)
        self.fields['aluno'].queryset = Aluno.objects.all().order_by('nome_completo')
        self.fields['turma'].queryset = Turma.objects.all().order_by('nome')
        
        # Adicionar classes para estilização
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        turma = cleaned_data.get('turma')
        
        # Verificar se já existe uma matrícula ativa para este aluno no mesmo ano
        if aluno and turma and self.instance.pk is None:  # Se for uma nova matrícula
            ano_letivo = cleaned_data.get('ano_letivo')
            matriculas_existentes = Matricula.objects.filter(
                aluno=aluno,
                ano_letivo=ano_letivo,
                status='ativo'
            )
            
            if matriculas_existentes.exists():
                self.add_error('aluno', 'Este aluno já possui uma matrícula ativa para o ano letivo informado.')
                
        return cleaned_data