from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Professor
from .forms import ProfessorForm


@login_required
def lista_professores(request):
    professores = Professor.objects.all().order_by('nome')
    return render(request, 'professor/lista_professores.html', {'professores': professores})

@login_required
def detalhe_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    return render(request, 'professor/detalhe_professor.html', {'professor': professor})

@login_required
def novo_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                professor = form.save(commit=True)  # Força o commit
                messages.success(request, f'Professor {professor.nome} criado com sucesso!')
                return redirect('professor:detalhe_professor', professor_id=professor.id)
            except Exception as e:
                messages.error(request, f'Erro ao salvar professor: {str(e)}')
                print(f'Erro ao salvar professor: {str(e)}')  # Log para debug
        else:
            print(f'Erros no formulário: {form.errors}')  # Log para debug
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProfessorForm()
    
    return render(request, 'professor/form_professor.html', {
        'form': form,
        'titulo': 'Novo Professor'
    })

@login_required
def editar_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dados do professor {professor.nome} atualizados com sucesso!')
            return redirect('professor:detalhe_professor', professor_cpf=professor.cpf)
    else:
        form = ProfessorForm(instance=professor)
    
    return render(request, 'professor/form_professor.html', {
        'form': form,
        'professor': professor,
        'titulo': 'Editar Professor'
    })

@login_required
def excluir_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    
    if request.method == 'POST':
        nome = professor.nome
        professor.delete()
        messages.success(request, f'Professor {nome} excluído com sucesso!')
        return redirect('professor:lista_professores')
    
    return render(request, 'professor/confirmar_exclusao.html', {'professor': professor})
