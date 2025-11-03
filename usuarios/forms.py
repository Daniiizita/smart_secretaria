from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'tipo', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'tipo', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
            
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome de usuário'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})