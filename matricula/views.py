from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Matricula, Turma
from .forms import MatriculaForm
from logs.utils import registrar_atividade

@login_required
def lista_matriculas(request):
    # Iniciar com todas as matrículas
    matriculas = Matricula.objects.all()
    
    # Aplicar filtros se fornecidos
    if 'ano_letivo' in request.GET and request.GET['ano_letivo']:
        matriculas = matriculas.filter(ano_letivo=request.GET['ano_letivo'])
        
    if 'status' in request.GET and request.GET['status']:
        matriculas = matriculas.filter(status=request.GET['status'])
        
    if 'turma' in request.GET and request.GET['turma']:
        matriculas = matriculas.filter(turma_id=request.GET['turma'])
    
    # Ordenar o resultado
    matriculas = matriculas.order_by('-data_matricula')
    
    # Obter dados para os filtros
    anos_letivos = Matricula.objects.values_list('ano_letivo', flat=True).distinct().order_by('-ano_letivo')
    turmas = Turma.objects.all().order_by('nome')
    status_choices = Matricula.STATUS_CHOICES
    
    return render(request, 'matricula/lista_matriculas.html', {
        'matriculas': matriculas,
        'anos_letivos': anos_letivos,
        'turmas': turmas,
        'status_choices': status_choices
    })

@login_required
def detalhe_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, id=matricula_id)
    return render(request, 'matricula/detalhe_matricula.html', {'matricula': matricula})

@login_required
def nova_matricula(request):
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save()
            
            # Registrar atividade de criação
            registrar_atividade(
                usuario=request.user,
                acao="Criação de Matrícula",
                descricao_detalhada=f"Matrícula do aluno {matricula.aluno.nome_completo} na turma {matricula.turma.nome} foi criada."
            )
            
            messages.success(request, f'Matrícula do aluno {matricula.aluno.nome_completo} criada com sucesso!')
            return redirect('matricula:detalhe_matricula', matricula_id=matricula.id)
    else:
        form = MatriculaForm()
    
    return render(request, 'matricula/form_matricula.html', {
        'form': form,
        'titulo': 'Nova Matrícula'
    })

@login_required
def editar_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance=matricula)
        if form.is_valid():
            matricula_atualizada = form.save()
            
            # Registrar atividade de atualização
            registrar_atividade(
                usuario=request.user,
                acao="Atualização de Matrícula",
                descricao_detalhada=f"Matrícula do aluno {matricula.aluno.nome_completo} foi atualizada."
            )
            
            messages.success(request, f'Matrícula do aluno {matricula.aluno.nome_completo} atualizada com sucesso!')
            return redirect('matricula:detalhe_matricula', matricula_id=matricula.id)
    else:
        form = MatriculaForm(instance=matricula)
    
    return render(request, 'matricula/form_matricula.html', {
        'form': form,
        'matricula': matricula,
        'titulo': 'Editar Matrícula'
    })

@login_required
def excluir_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    if request.method == 'POST':
        aluno_nome = matricula.aluno.nome_completo
        
        # Registrar atividade de exclusão
        registrar_atividade(
            usuario=request.user,
            acao="Exclusão de Matrícula",
            descricao_detalhada=f"Matrícula do aluno {aluno_nome} na turma {matricula.turma.nome} foi excluída."
        )
        
        matricula.delete()
        messages.success(request, f'Matrícula do aluno {aluno_nome} excluída com sucesso!')
        return redirect('matricula:lista_matriculas')
    
    return render(request, 'matricula/confirmar_exclusao.html', {'matricula': matricula})

@login_required
def mudar_status_matricula(request, matricula_id, novo_status):
    matricula = get_object_or_404(Matricula, id=matricula_id)
    status_antigo = matricula.status
    
    if novo_status in dict(Matricula.STATUS_CHOICES):
        matricula.status = novo_status
        matricula.save()
        
        # Registrar atividade de mudança de status
        registrar_atividade(
            usuario=request.user,
            acao="Alteração de Status de Matrícula",
            descricao_detalhada=f"Status da matrícula do aluno {matricula.aluno.nome_completo} alterado de {status_antigo} para {novo_status}."
        )
        
        messages.success(request, f'Status da matrícula alterado para {dict(Matricula.STATUS_CHOICES)[novo_status]}!')
    else:
        messages.error(request, f'Status inválido!')
        
    return redirect('matricula:detalhe_matricula', matricula_id=matricula.id)
