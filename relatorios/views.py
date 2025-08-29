from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import openpyxl
from aluno.models import Aluno
from turma.models import Turma, SERIE_CHOICES, NIVEL_CHOICES
import re

def normalizar_nome_arquivo(nome):
    """
    Normaliza o nome da turma para ser usado como nome de arquivo
    removendo caracteres especiais e substituindo espaços por underscore
    """
    # Remove caracteres especiais e acentos
    nome = re.sub(r'[^\w\s]', '', nome)
    # Substitui espaços por underscores
    nome = nome.replace(' ', '_')
    return nome

@login_required
def alunos_por_turma_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Alunos por Turma"
    
    # Cabeçalhos mais específicos
    ws.append(["Série/Ano", "Turma", "Nível de Ensino", "Sigla", "Período", "Ano Letivo", 
               "Aluno", "Data de Nascimento", "Telefone"])

    for turma in Turma.objects.all():
        # Obtendo o texto da série a partir das escolhas
        serie_texto = dict(SERIE_CHOICES).get(turma.serie, f"{turma.serie}º Ano")
        partes = serie_texto.split(' - ')
        serie_ano = partes[0] if len(partes) > 1 else serie_texto
        
        # Obtendo o texto do nível de ensino
        nivel_ensino = dict(NIVEL_CHOICES).get(turma.nivel_ensino_sigla, "")
        
        alunos = Aluno.objects.filter(turma=turma)
        for aluno in alunos:
            ws.append([
                serie_ano,                  # Série/Ano (ex: "1º Ano" ou "2º Período")
                turma.turma_letra,          # Letra da Turma (ex: "A", "B")
                nivel_ensino,               # Nível de Ensino por extenso
                turma.nivel_ensino_sigla,   # Sigla do Nível (EFI, EFII, etc)
                turma.periodo,              # Período (Manhã, Tarde, etc)
                turma.ano,                  # Ano Letivo
                aluno.nome_completo,        # Nome do Aluno
                aluno.data_nascimento,      # Data de Nascimento
                aluno.telefone_contato      # Telefone
            ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=alunos_por_turma.xlsx'
    wb.save(response)
    return response

@login_required
def alunos_da_turma_excel(request, turma_id):
    turma = Turma.objects.get(pk=turma_id)
    
    # Obtendo o texto da série a partir das escolhas
    serie_texto = dict(SERIE_CHOICES).get(turma.serie, f"{turma.serie}º Ano")
    partes = serie_texto.split(' - ')
    serie_ano = partes[0] if len(partes) > 1 else serie_texto
    
    # Obtendo o texto do nível de ensino
    nivel_ensino = dict(NIVEL_CHOICES).get(turma.nivel_ensino_sigla, "")
    
    alunos = Aluno.objects.filter(turma=turma)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Alunos {serie_ano} {turma.turma_letra}"
    
    # Cabeçalhos mais específicos
    ws.append(["Série/Ano", "Turma", "Nível de Ensino", "Sigla", "Período", "Ano Letivo", 
               "Aluno", "Data de Nascimento", "Telefone"])

    for aluno in alunos:
        ws.append([
            serie_ano,                  # Série/Ano (ex: "1º Ano" ou "2º Período")
            turma.turma_letra,          # Letra da Turma (ex: "A", "B")
            nivel_ensino,               # Nível de Ensino por extenso
            turma.nivel_ensino_sigla,   # Sigla do Nível (EFI, EFII, etc)
            turma.periodo,              # Período (Manhã, Tarde, etc)
            turma.ano,                  # Ano Letivo
            aluno.nome_completo,        # Nome do Aluno
            aluno.data_nascimento,      # Data de Nascimento
            aluno.telefone_contato      # Telefone
        ])

    # Criar um nome de arquivo amigável baseado no nome da turma
    nome_arquivo = normalizar_nome_arquivo(f"{serie_ano}_{turma.turma_letra}_{turma.nivel_ensino_sigla}")
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=alunos_{nome_arquivo}.xlsx'
    wb.save(response)
    return response
