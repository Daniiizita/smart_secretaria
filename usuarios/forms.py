from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    # Modificação aqui: iniciamos com tipos restritos
    tipo = forms.ChoiceField(
        choices=(
            ('professor', 'Professor'),
            ('aluno', 'Aluno'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'tipo')
    
    def __init__(self, *args, **kwargs):
        # Recebemos o user atual como parâmetro opcional
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Configuramos os widgets para melhorar a aparência
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Adaptar as opções baseado em quem está criando o usuário
        if user and user.is_authenticated:
            if user.tipo == 'admin' or user.is_superuser:
                # Admin pode criar qualquer tipo de usuário
                self.fields['tipo'].choices = CustomUser.TIPOS_USUARIO
            elif user.tipo == 'diretor':
                # Diretor tem as mesmas permissões do admin
                self.fields['tipo'].choices = CustomUser.TIPOS_USUARIO
            elif user.tipo == 'secretario':
                # Secretário pode criar todos exceto admin
                self.fields['tipo'].choices = [
                    choice for choice in CustomUser.TIPOS_USUARIO
                    if choice[0] not in ['admin', 'diretor']
                ]

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomUserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    # Campo de tipo (será preenchido dinamicamente no __init__)
    tipo = forms.ChoiceField(
        choices=CustomUser.TIPOS_USUARIO,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'tipo', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Recebemos o user atual como parâmetro opcional
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Adaptar as opções baseado em quem está editando o usuário
        if user and user.is_authenticated:
            if user.tipo == 'admin' or user.is_superuser:
                # Admin pode editar para qualquer tipo de usuário
                self.fields['tipo'].choices = CustomUser.TIPOS_USUARIO
            elif user.tipo == 'diretor':
                # Diretor tem as mesmas permissões do admin
                self.fields['tipo'].choices = CustomUser.TIPOS_USUARIO
            elif user.tipo == 'secretario':
                # Secretário pode editar todos exceto admin e diretor
                self.fields['tipo'].choices = [
                    choice for choice in CustomUser.TIPOS_USUARIO
                    if choice[0] not in ['admin', 'diretor']
                ]
                
                # Se o usuário sendo editado é admin ou diretor, desabilitar o campo
                instance = kwargs.get('instance')
                if instance and instance.tipo in ['admin', 'diretor']:
                    self.fields['tipo'].disabled = True