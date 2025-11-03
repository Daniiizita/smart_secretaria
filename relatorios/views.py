from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import openpyxl
import re
from aluno.models import Aluno
from turma.models import Turma, SERIE_CHOICES, NIVEL_CHOICES

# Imports para PDF
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

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

# Função existente para Excel
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

# Nova função para PDF
@login_required
def alunos_por_turma_pdf(request):
    # Criando um buffer de memória para o PDF
    buffer = BytesIO()
    
    # Configurando o documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        title="Alunos por Turma"
    )
    
    # Lista para armazenar elementos do PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    
    # Título do relatório
    title = Paragraph("Relatório de Alunos por Turma", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.25*inch))
    
    # Cabeçalhos da tabela
    headers = ["Série/Ano", "Turma", "Nível de Ensino", "Sigla", "Período", "Ano Letivo", 
               "Aluno", "Data de Nascimento", "Telefone"]
    
    # Lista para armazenar os dados da tabela
    data = [headers]
    
    # Populando os dados
    for turma in Turma.objects.all().order_by('serie', 'turma_letra'):
        # Obtendo o texto da série a partir das escolhas
        serie_texto = dict(SERIE_CHOICES).get(turma.serie, f"{turma.serie}º Ano")
        partes = serie_texto.split(' - ')
        serie_ano = partes[0] if len(partes) > 1 else serie_texto
        
        # Obtendo o texto do nível de ensino
        nivel_ensino = dict(NIVEL_CHOICES).get(turma.nivel_ensino_sigla, "")
        
        alunos = Aluno.objects.filter(turma=turma).order_by('nome_completo')
        
        if not alunos:
            # Se não há alunos, adiciona uma linha indicando isso
            data.append([
                serie_ano, turma.turma_letra, nivel_ensino, 
                turma.nivel_ensino_sigla, turma.periodo, turma.ano,
                "Sem alunos", "", ""
            ])
        else:
            for aluno in alunos:
                data.append([
                    serie_ano,
                    turma.turma_letra,
                    nivel_ensino,
                    turma.nivel_ensino_sigla,
                    turma.periodo,
                    turma.ano,
                    aluno.nome_completo,
                    aluno.data_nascimento.strftime("%d/%m/%Y") if aluno.data_nascimento else "",
                    aluno.telefone_contato
                ])
    
    # Criando a tabela
    table = Table(data)
    
    # Estilo da tabela
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    table.setStyle(table_style)
    elements.append(table)
    
    # Construindo o documento
    doc.build(elements)
    
    # Obtendo o PDF do buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Criando a resposta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=alunos_por_turma.pdf'
    response.write(pdf)
    
    return response

@login_required
def alunos_da_turma_pdf(request, turma_id):
    turma = Turma.objects.get(pk=turma_id)
    
    # Criando um buffer de memória para o PDF
    buffer = BytesIO()
    
    # Configurando o documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        title=f"Alunos da Turma {turma.nome}"
    )
    
    # Lista para armazenar elementos do PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    
    # Obtendo o texto da série a partir das escolhas
    serie_texto = dict(SERIE_CHOICES).get(turma.serie, f"{turma.serie}º Ano")
    partes = serie_texto.split(' - ')
    serie_ano = partes[0] if len(partes) > 1 else serie_texto
    
    # Obtendo o texto do nível de ensino
    nivel_ensino = dict(NIVEL_CHOICES).get(turma.nivel_ensino_sigla, "")
    
    # Título do relatório
    title = Paragraph(f"Relatório de Alunos - {serie_ano} {turma.turma_letra}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.25*inch))
    
    # Informações da turma
    turma_info = f"Turma: {turma.nome} | Nível: {nivel_ensino} ({turma.nivel_ensino_sigla}) | Período: {turma.periodo} | Ano Letivo: {turma.ano}"
    elements.append(Paragraph(turma_info, styles['Normal']))
    elements.append(Spacer(1, 0.25*inch))
    
    # Cabeçalhos da tabela
    headers = ["Aluno", "Data de Nascimento", "Telefone"]
    
    # Lista para armazenar os dados da tabela
    data = [headers]
    
    # Populando os dados
    alunos = Aluno.objects.filter(turma=turma).order_by('nome_completo')
    
    if not alunos:
        # Se não há alunos, adiciona uma linha indicando isso
        data.append(["Sem alunos cadastrados", "", ""])
    else:
        for aluno in alunos:
            data.append([
                aluno.nome_completo,
                aluno.data_nascimento.strftime("%d/%m/%Y") if aluno.data_nascimento else "",
                aluno.telefone_contato
            ])
    
    # Criando a tabela
    table = Table(data)
    
    # Estilo da tabela
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    table.setStyle(table_style)
    elements.append(table)
    
    # Construindo o documento
    doc.build(elements)
    
    # Obtendo o PDF do buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Criando a resposta HTTP
    nome_arquivo = normalizar_nome_arquivo(f"{serie_ano}_{turma.turma_letra}_{turma.nivel_ensino_sigla}")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=alunos_{nome_arquivo}.pdf'
    response.write(pdf)
    
    return response
