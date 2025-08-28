from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Documento
from aluno.models import Aluno
from .forms import DocumentoForm, DocumentoAlunoForm
from logs.utils import registrar_atividade

@login_required
def lista_documentos(request):
    # Buscar todos os alunos para o filtro
    alunos = Aluno.objects.all().order_by('nome_completo')
    
    # Filtrar documentos por aluno se o parâmetro for fornecido
    aluno_id = request.GET.get('aluno_id')
    
    if aluno_id:
        aluno = get_object_or_404(Aluno, id=aluno_id)
        documentos = Documento.objects.filter(aluno=aluno).order_by('-data_emissao')
        return render(request, 'documentos/lista_documentos.html', {
            'documentos': documentos,
            'aluno': aluno,
            'alunos': alunos,
            'aluno_id': int(aluno_id) if aluno_id.isdigit() else None
        })
    else:
        documentos = Documento.objects.all().order_by('-data_emissao')
        return render(request, 'documentos/lista_documentos.html', {
            'documentos': documentos,
            'alunos': alunos,
            'aluno_id': None
        })

@login_required
def detalhe_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    return render(request, 'documentos/detalhe_documento.html', {'documento': documento})

@login_required
def novo_documento(request):
    # Verificar se há um aluno especificado
    aluno_id = request.GET.get('aluno_id')
    aluno = None
    
    if aluno_id:
        aluno = get_object_or_404(Aluno, id=aluno_id)
        
    if request.method == 'POST':
        if aluno:
            form = DocumentoAlunoForm(request.POST)
            if form.is_valid():
                documento = form.save(commit=False)
                documento.aluno = aluno
                documento.save()
                
                # Registrar atividade
                registrar_atividade(
                    usuario=request.user,
                    acao="Criação de Documento",
                    descricao_detalhada=f"Documento '{documento.get_tipo_display()}' criado para o aluno {aluno.nome_completo}."
                )
                
                messages.success(request, f'Documento criado com sucesso para {aluno.nome_completo}!')
                return redirect('documentos:detalhe_documento', documento_id=documento.id)
        else:
            form = DocumentoForm(request.POST)
            if form.is_valid():
                documento = form.save()
                
                # Registrar atividade
                registrar_atividade(
                    usuario=request.user,
                    acao="Criação de Documento",
                    descricao_detalhada=f"Documento '{documento.get_tipo_display()}' criado para o aluno {documento.aluno.nome_completo}."
                )
                
                messages.success(request, f'Documento criado com sucesso para {documento.aluno.nome_completo}!')
                return redirect('documentos:detalhe_documento', documento_id=documento.id)
    else:
        if aluno:
            form = DocumentoAlunoForm(initial={'data_emissao': timezone.now().date()})
            titulo = f'Novo Documento para {aluno.nome_completo}'
        else:
            form = DocumentoForm(initial={'data_emissao': timezone.now().date()})
            titulo = 'Novo Documento'
    
    return render(request, 'documentos/form_documento.html', {
        'form': form,
        'aluno': aluno,
        'titulo': titulo
    })

@login_required
def editar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    aluno = documento.aluno
    
    if request.method == 'POST':
        form = DocumentoAlunoForm(request.POST, instance=documento)
        if form.is_valid():
            documento = form.save()
            
            # Registrar atividade
            registrar_atividade(
                usuario=request.user,
                acao="Edição de Documento",
                descricao_detalhada=f"Documento '{documento.get_tipo_display()}' do aluno {aluno.nome_completo} foi editado."
            )
            
            messages.success(request, f'Documento atualizado com sucesso!')
            return redirect('documentos:detalhe_documento', documento_id=documento.id)
    else:
        form = DocumentoAlunoForm(instance=documento)
    
    return render(request, 'documentos/form_documento.html', {
        'form': form,
        'documento': documento,
        'aluno': aluno,
        'titulo': f'Editar Documento de {aluno.nome_completo}'
    })

@login_required
def excluir_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    aluno = documento.aluno
    
    if request.method == 'POST':
        tipo_documento = documento.get_tipo_display()
        
        # Registrar atividade
        registrar_atividade(
            usuario=request.user,
            acao="Exclusão de Documento",
            descricao_detalhada=f"Documento '{tipo_documento}' do aluno {aluno.nome_completo} foi excluído."
        )
        
        documento.delete()
        messages.success(request, f'Documento excluído com sucesso!')
        
        # Redirecionar de volta para a lista de documentos do aluno se veio de lá
        if 'aluno_id' in request.GET:
            return redirect('documentos:lista_documentos', aluno_id=aluno.id)
        else:
            return redirect('documentos:lista_documentos')
    
    return render(request, 'documentos/confirmar_exclusao.html', {
        'documento': documento,
        'aluno': aluno
    })

@login_required
def imprimir_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    
    try:
        # Tente registrar a atividade
        registrar_atividade(
            usuario=request.user,
            acao="Impressão de Documento",
            descricao_detalhada=f"Documento '{documento.get_tipo_display()}' do aluno {documento.aluno.nome_completo} foi impresso/visualizado."
        )
    except Exception as e:
        # Se falhar, apenas registre no console e continue
        print(f"Erro ao registrar atividade: {str(e)}")
        # Opcionalmente, adicione uma mensagem para o usuário
        messages.warning(request, "O documento será exibido, mas ocorreu um erro ao registrar esta atividade.")
    
    return render(request, 'documentos/imprimir_documento.html', {'documento': documento})
