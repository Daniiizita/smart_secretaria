from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import Aluno
from .forms import AlunoForm
from usuarios.models import ConviteRegistro
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

@login_required
def lista_alunos(request):
    alunos = Aluno.objects.all().order_by('nome_completo')
    return render(request, 'aluno/lista_alunos.html', {'alunos': alunos})

@login_required
def detalhe_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    return render(request, 'aluno/detalhe_aluno.html', {'aluno': aluno})

@login_required
def novo_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            aluno = form.save()
            messages.success(request, f'Aluno {aluno.nome_completo} criado com sucesso!')
            return redirect('aluno:detalhe_aluno', aluno_id=aluno.id)
    else:
        form = AlunoForm()
    
    return render(request, 'aluno/form_aluno.html', {
        'form': form,
        'titulo': 'Novo Aluno'
    })

@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dados do aluno {aluno.nome_completo} atualizados com sucesso!')
            return redirect('aluno:detalhe_aluno', aluno_id=aluno.id)
    else:
        form = AlunoForm(instance=aluno)
    
    return render(request, 'aluno/form_aluno.html', {
        'form': form,
        'aluno': aluno,
        'titulo': 'Editar Aluno'
    })

@login_required
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    if request.method == 'POST':
        nome = aluno.nome_completo
        aluno.delete()
        messages.success(request, f'Aluno {nome} excluído com sucesso!')
        return redirect('aluno:lista_alunos')
    
    return render(request, 'aluno/confirmar_exclusao.html', {'aluno': aluno})

@login_required
@user_passes_test(lambda u: u.tipo in ['admin', 'diretor', 'secretario'])
def gerar_convite_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, "É necessário fornecer um email.")
            return redirect('aluno:detalhe_aluno', aluno_id=aluno.id)
        
        # Criar o convite
        convite = ConviteRegistro.gerar_convite(aluno, email, request.user)
        
        # Construir o link de convite
        link_convite = request.build_absolute_uri(
            reverse('usuarios:registrar_com_convite', kwargs={'token': convite.token})
        )
        
        # Enviar email (se configurado)
        try:
            send_mail(
                'Convite para cadastro no sistema escolar',
                f'Olá {aluno.nome_completo},\n\nVocê foi convidado para criar uma conta no sistema escolar. '
                f'Para se registrar, acesse o link: {link_convite}\n\n'
                f'Este link é válido por 7 dias.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, f"Convite enviado para {email}")
        except Exception as e:
            # Caso o email não esteja configurado, exibe o link para copiar
            messages.warning(request, f"Não foi possível enviar o email. Copie o link: {link_convite}")
        
        return redirect('aluno:detalhe_aluno', aluno_id=aluno.id)
    
    return render(request, 'aluno/gerar_convite.html', {
        'aluno': aluno
    })

@login_required
@user_passes_test(lambda u: u.tipo in ['admin', 'diretor', 'secretario'])
def listar_convites(request):
    convites = ConviteRegistro.objects.all().order_by('-criado_em')
    return render(request, 'aluno/listar_convites.html', {'convites': convites})