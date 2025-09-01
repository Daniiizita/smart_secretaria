from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from permissoes.services import associar_usuario_ao_grupo

def registro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            
            # Associar ao grupo conforme o tipo de usuário
            tipo_usuario = form.cleaned_data.get('tipo')
            associar_usuario_ao_grupo(usuario, tipo_usuario)
            
            login(request, usuario)
            messages.success(request, "Registro bem-sucedido!")
            return redirect('core:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Bem-vindo, {username}!")
                # Redirecionar para a página que o usuário estava tentando acessar
                next_url = request.GET.get('next', 'core:index')
                return redirect(next_url)
            else:
                messages.error(request, "Nome de usuário ou senha inválidos.")
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    messages.info(request, "Você saiu com sucesso!")
    return redirect('usuarios:login')
