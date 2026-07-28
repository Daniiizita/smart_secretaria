from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Disciplina
from .forms import DisciplinaForm
from logs.utils import registrar_atividade  # Se estiver utilizando este módulo

@login_required
def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all().order_by('nome')
    return render(request, 'disciplinas/lista_disciplinas.html', {'disciplinas': disciplinas})

@login_required
def detalhe_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    return render(request, 'disciplinas/detalhe_disciplina.html', {'disciplina': disciplina})

@login_required
def nova_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save()
            
            # Registrar atividade
            registrar_atividade(
                usuario=request.user,
                acao="Criação de Disciplina",
                descricao_detalhada=f"Disciplina {disciplina.nome} foi criada."
            )
            
            messages.success(request, f'Disciplina {disciplina.nome} criada com sucesso!')
            return redirect('disciplinas:detalhe_disciplina', disciplina_id=disciplina.id)
    else:
        form = DisciplinaForm()
    
    return render(request, 'disciplinas/form_disciplina.html', {
        'form': form,
        'titulo': 'Nova Disciplina'
    })

@login_required
def editar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            
            # Registrar atividade
            registrar_atividade(
                usuario=request.user,
                acao="Atualização de Disciplina",
                descricao_detalhada=f"Disciplina {disciplina.nome} foi atualizada."
            )
            
            messages.success(request, f'Disciplina {disciplina.nome} atualizada com sucesso!')
            return redirect('disciplinas:detalhe_disciplina', disciplina_id=disciplina.id)
    else:
        form = DisciplinaForm(instance=disciplina)
    
    return render(request, 'disciplinas/form_disciplina.html', {
        'form': form,
        'disciplina': disciplina,
        'titulo': 'Editar Disciplina'
    })

@login_required
def excluir_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    
    # Verificar se há professores associados
    professores_associados = disciplina.professor_set.exists()
    
    if request.method == 'POST':
        if professores_associados:
            messages.error(request, f'Não é possível excluir a disciplina {disciplina.nome} pois existem professores associados a ela.')
            return redirect('disciplinas:detalhe_disciplina', disciplina_id=disciplina.id)
        else:
            nome = disciplina.nome
            disciplina.delete()
            
            # Registrar atividade
            registrar_atividade(
                usuario=request.user,
                acao="Exclusão de Disciplina",
                descricao_detalhada=f"Disciplina {nome} foi excluída."
            )
            
            messages.success(request, f'Disciplina {nome} excluída com sucesso!')
            return redirect('disciplinas:lista_disciplinas')
    
    return render(request, 'disciplinas/confirmar_exclusao.html', {
        'disciplina': disciplina,
        'professores_associados': professores_associados
    })
