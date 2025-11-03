from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Aluno
from .forms import AlunoForm

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