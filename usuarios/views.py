from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserEditForm
from usuarios.models import CustomUser
from permissoes.services import associar_usuario_ao_grupo
from .models import ConviteRegistro

def registro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, user=request.user)
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
        form = CustomUserCreationForm(user=request.user)
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.tipo in ['admin', 'diretor', 'secretario'])
def criar_usuario(request):
    """View para admins, diretores e secretários criarem usuários"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, user=request.user)
        if form.is_valid():
            usuario = form.save()
            
            # Associar ao grupo conforme o tipo de usuário
            tipo_usuario = form.cleaned_data.get('tipo')
            associar_usuario_ao_grupo(usuario, tipo_usuario)
            
            messages.success(request, f"Usuário {usuario.username} criado com sucesso!")
            return redirect('usuarios:listar_usuarios')
    else:
        form = CustomUserCreationForm(user=request.user)
    
    return render(request, 'usuarios/criar_usuario.html', {
        'form': form,
        'titulo': 'Criar Novo Usuário'
    })

@login_required
@user_passes_test(lambda u: u.tipo in ['admin', 'diretor', 'secretario'])
def listar_usuarios(request):
    """View para listar todos os usuários (para admins e secretários)"""
    users = CustomUser.objects.all().order_by('username')
    return render(request, 'usuarios/listar_usuarios.html', {'users': users})

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

@login_required
@user_passes_test(lambda u: u.tipo in ['admin', 'diretor', 'secretario'])
def editar_usuario(request, user_id):
    """View para editar usuários existentes"""
    user_para_editar = get_object_or_404(CustomUser, id=user_id)
    
    # Verificação de permissão: secretários não podem editar admins ou diretores
    if request.user.tipo == 'secretario' and user_para_editar.tipo in ['admin', 'diretor']:
        messages.error(request, "Você não tem permissão para editar este tipo de usuário.")
        return redirect('usuarios:listar_usuarios')
    
    if request.method == 'POST':
        # Usamos um formulário diferente para edição (sem alteração de senha)
        form = CustomUserEditForm(request.POST, instance=user_para_editar, user=request.user)
        if form.is_valid():
            # Salvar as alterações
            usuario = form.save()
            
            # Associar ao grupo conforme o tipo de usuário (caso tenha mudado)
            tipo_usuario = form.cleaned_data.get('tipo')
            associar_usuario_ao_grupo(usuario, tipo_usuario)
            
            messages.success(request, f"Usuário {usuario.username} atualizado com sucesso!")
            return redirect('usuarios:listar_usuarios')
    else:
        form = CustomUserEditForm(instance=user_para_editar, user=request.user)
    
    return render(request, 'usuarios/editar_usuario.html', {
        'form': form,
        'usuario': user_para_editar,
        'titulo': f'Editar Usuário: {user_para_editar.username}'
    })

@login_required
@user_passes_test(lambda u: u.tipo in ['admin', 'diretor', 'secretario'])
def excluir_usuario(request, user_id):
    """View para excluir usuários"""
    user_para_excluir = get_object_or_404(CustomUser, id=user_id)
    
    # Verificação de permissão: secretários não podem excluir admins ou diretores
    if request.user.tipo == 'secretario' and user_para_excluir.tipo in ['admin', 'diretor']:
        messages.error(request, "Você não tem permissão para excluir este tipo de usuário.")
        return redirect('usuarios:listar_usuarios')
    
    # Não permitir que um usuário exclua a si mesmo
    if user_para_excluir.id == request.user.id:
        messages.error(request, "Você não pode excluir seu próprio usuário.")
        return redirect('usuarios:listar_usuarios')
        
    if request.method == 'POST':
        username = user_para_excluir.username
        user_para_excluir.delete()
        messages.success(request, f"Usuário {username} excluído com sucesso!")
        return redirect('usuarios:listar_usuarios')
    
    return render(request, 'usuarios/confirmar_exclusao.html', {
        'usuario': user_para_excluir
    })

# Adicione esta nova view para registro com convite
def registrar_com_convite(request, token):
    # Verificar se o token é válido
    try:
        convite = ConviteRegistro.objects.get(token=token)
        if not convite.esta_valido():
            messages.error(request, "Este convite expirou ou já foi usado.")
            return redirect('usuarios:login')
    except ConviteRegistro.DoesNotExist:
        messages.error(request, "Convite inválido.")
        return redirect('usuarios:login')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # Forçar o tipo como aluno
        form.fields['tipo'].initial = 'aluno'
        form.fields['tipo'].widget.attrs['readonly'] = True
        
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.email = convite.email
            usuario.tipo = 'aluno'  # Garantir que é aluno
            usuario.save()
            
            # Associar ao grupo
            associar_usuario_ao_grupo(usuario, 'aluno')
            
            # Associar ao perfil do aluno
            aluno = convite.aluno
            aluno.usuario = usuario
            aluno.save()
            
            # Marcar convite como usado
            convite.usado = True
            convite.save()
            
            # Autenticar e redirecionar
            login(request, usuario)
            messages.success(request, "Conta criada com sucesso! Bem-vindo ao sistema escolar.")
            return redirect('core:index')
    else:
        form = CustomUserCreationForm(initial={'tipo': 'aluno', 'email': convite.email})
        # Restringir opções de tipo e tornar o campo readonly
        form.fields['tipo'].choices = [('aluno', 'Aluno')]
        form.fields['tipo'].widget.attrs['readonly'] = True
    
    return render(request, 'usuarios/registro_com_convite.html', {
        'form': form,
        'convite': convite
    })