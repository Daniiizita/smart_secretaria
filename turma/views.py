from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Turma
from .forms import TurmaForm
from aluno.models import Aluno

@login_required
def lista_turmas(request):
    turmas = Turma.objects.all().order_by('ano', 'serie', 'turma_letra')
    return render(request, 'turma/lista_turmas.html', {'turmas': turmas})

@login_required
def detalhe_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    alunos = Aluno.objects.filter(turma=turma).order_by('nome_completo')
    return render(request, 'turma/detalhe_turma.html', {
        'turma': turma,
        'alunos': alunos
    })

@login_required
def nova_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, f'Turma {turma.nome} criada com sucesso!')
            return redirect('turma:detalhe_turma', turma_id=turma.id)
    else:
        form = TurmaForm()
    
    return render(request, 'turma/form_turma.html', {
        'form': form,
        'titulo': 'Nova Turma'
    })

@login_required
def editar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dados da turma {turma.nome} atualizados com sucesso!')
            return redirect('turma:detalhe_turma', turma_id=turma.id)
    else:
        form = TurmaForm(instance=turma)
    
    return render(request, 'turma/form_turma.html', {
        'form': form,
        'turma': turma,
        'titulo': 'Editar Turma'
    })

@login_required
def excluir_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    
    # Verificar se existem alunos na turma
    alunos_na_turma = Aluno.objects.filter(turma=turma).exists()
    
    if request.method == 'POST':
        if alunos_na_turma:
            messages.error(request, f'Não é possível excluir a turma {turma.nome} pois existem alunos matriculados nela.')
            return redirect('turma:detalhe_turma', turma_id=turma.id)
        else:
            nome = turma.nome
            turma.delete()
            messages.success(request, f'Turma {nome} excluída com sucesso!')
            return redirect('turma:lista_turmas')
    
    return render(request, 'turma/confirmar_exclusao.html', {
        'turma': turma,
        'alunos_na_turma': alunos_na_turma
    })
