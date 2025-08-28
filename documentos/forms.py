from django import forms
from .models import Documento
from aluno.models import Aluno

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['aluno', 'tipo', 'data_emissao', 'conteudo']
        widgets = {
            'data_emissao': forms.DateInput(attrs={'type': 'date'}),
            'conteudo': forms.Textarea(attrs={'rows': 10}),
        }
        
    def __init__(self, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)
        # Ordenar alunos pelo nome para facilitar a busca
        self.fields['aluno'].queryset = Aluno.objects.all().order_by('nome_completo')
        
        # Adicionar classes para estilização
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
class DocumentoAlunoForm(forms.ModelForm):
    """
    Formulário específico para quando já sabemos o aluno (não mostra o campo de seleção)
    """
    class Meta:
        model = Documento
        fields = ['tipo', 'data_emissao', 'conteudo']
        widgets = {
            'data_emissao': forms.DateInput(attrs={'type': 'date'}),
            'conteudo': forms.Textarea(attrs={'rows': 10}),
        }
        
    def __init__(self, *args, **kwargs):
        super(DocumentoAlunoForm, self).__init__(*args, **kwargs)
        
        # Adicionar classes para estilização
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})