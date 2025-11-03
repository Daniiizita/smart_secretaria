# calendars/views.py
from __future__ import annotations
import calendar
from datetime import datetime, date, time, timedelta
from typing import Dict, List
from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Evento
from .forms import EventoForm
from datetime import datetime, date, time, timedelta

@login_required
def lista_eventos(request):
    # Obtém data atual para filtrar eventos
    hoje = timezone.now()
    
    # Eventos passados (que já ocorrereram)
    eventos_passados = Evento.objects.filter(data_fim__lt=hoje).order_by('-data_inicio')
    
    # Eventos futuros (que ainda vão ocorrer)
    eventos_futuros = Evento.objects.filter(data_inicio__gte=hoje).order_by('data_inicio')
    
    # Eventos em andamento (que estão acontecendo agora)
    eventos_andamento = Evento.objects.filter(
        data_inicio__lte=hoje,
        data_fim__gte=hoje
    ).order_by('data_fim')
    
    context = {
        'eventos_passados': eventos_passados,
        'eventos_futuros': eventos_futuros,
        'eventos_andamento': eventos_andamento,
        'hoje': hoje,
    }
    
    return render(request, 'calendario/lista_eventos.html', context)

@login_required
def detalhe_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'calendario/detalhe_evento.html', {'evento': evento})

@login_required
def novo_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()
            messages.success(request, f'Evento "{evento.titulo}" criado com sucesso!')
            return redirect('calendario:detalhe_evento', pk=evento.pk)
    else:
        form = EventoForm()
    
    return render(request, 'calendario/form_evento.html', {
        'form': form,
        'titulo': 'Novo Evento'
    })

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            evento = form.save()
            messages.success(request, f'Evento "{evento.titulo}" atualizado com sucesso!')
            return redirect('calendario:detalhe_evento', pk=evento.pk)
    else:
        form = EventoForm(instance=evento)
    
    return render(request, 'calendario/form_evento.html', {
        'form': form,
        'evento': evento,
        'titulo': 'Editar Evento'
    })

@login_required
def excluir_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    
    if request.method == 'POST':
        titulo = evento.titulo
        evento.delete()
        messages.success(request, f'Evento "{titulo}" excluído com sucesso!')
        return redirect('calendario:lista_eventos')
    
    return render(request, 'calendario/confirmar_exclusao.html', {'evento': evento})

@login_required
def calendario_mensal(request):
    """
    Gera a grade do calendário do mês (semanas x dias) e agrega eventos por data.
    O template itera e renderiza.
    """
    # 1) Mês/ano alvo (fallback = hoje)
    tz_now = timezone.localtime()
    mes = int(request.GET.get("mes", tz_now.month))
    ano = int(request.GET.get("ano", tz_now.year))

    # 2) Limites do mês (datas “naive” para grade; limites aware para query)
    #    Primeiro e último dia do mês em date (sem tz) p/ facilitar comparações de calendário.
    first_day = date(ano, mes, 1)
    # Truque: ir para dia 28, somar 4 dias, cai no próximo mês, depois voltar para o dia 1 do próximo e subtrair 1
    next_month = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)
    last_day = next_month - timedelta(days=1)

    # 3) Janela-aware para buscar eventos que "tocam" o mês (sobreposição)
    month_start_dt = timezone.make_aware(datetime.combine(first_day, time.min))
    month_end_dt = timezone.make_aware(datetime.combine(last_day, time.max))

    # 4) Buscar eventos que tenham qualquer interseção com o mês
    #    start <= fim_do_mês E end >= início_do_mês
    eventos = (
        Evento.objects.filter(
            data_inicio__lte=month_end_dt,
            data_fim__gte=month_start_dt,
        )
        .order_by("data_inicio", "data_fim")
    )

    # 5) Montar dicionário de eventos por cada data do mês (inclui eventos multidiários)
    eventos_por_data: Dict[date, List[Evento]] = defaultdict(list)

    for ev in eventos:
        # Normaliza para datas (corta a parte de horário)
        ev_start_d = timezone.localtime(ev.data_inicio).date()
        ev_end_d = timezone.localtime(ev.data_fim).date()

        # Restringe o espalhamento ao intervalo do mês alvo
        span_start = max(ev_start_d, first_day)
        span_end = min(ev_end_d, last_day)

        # Se por qualquer motivo não houver interseção, pula
        if span_start > span_end:
            continue

        # Espalha o evento por todos os dias entre span_start e span_end
        day_ptr = span_start
        while day_ptr <= span_end:
            eventos_por_data[day_ptr].append(ev)
            day_ptr += timedelta(days=1)

    # 6) Gera matriz de semanas do mês com `date` completos (inclui “sobras” de outros meses)
    cal = calendar.Calendar(firstweekday=6)  # 6 = domingo primeiro; troque para 0 se quiser segunda
    weeks = cal.monthdatescalendar(ano, mes)  # List[List[date]]

    # 7) Enriquecer semanas com bandeiras e eventos -> o template só itera
    weeks_enriched = []
    for week in weeks:
        row = []
        for d in week:
            row.append(
                {
                    "date": d,                          # datetime.date
                    "in_month": (d.month == mes),       # célula do próprio mês?
                    "events": eventos_por_data.get(d, [])
                }
            )
        weeks_enriched.append(row)

    # 8) Navegação (mês anterior/próximo)
    if mes == 1:
        mes_anterior, ano_anterior = 12, ano - 1
    else:
        mes_anterior, ano_anterior = mes - 1, ano

    if mes == 12:
        mes_seguinte, ano_seguinte = 1, ano + 1
    else:
        mes_seguinte, ano_seguinte = mes + 1, ano

    # 9) Dados auxiliares para selects
    meses = [
        (1, "Janeiro"), (2, "Fevereiro"), (3, "Março"),
        (4, "Abril"), (5, "Maio"), (6, "Junho"),
        (7, "Julho"), (8, "Agosto"), (9, "Setembro"),
        (10, "Outubro"), (11, "Novembro"), (12, "Dezembro"),
    ]
    nome_mes = meses[mes - 1][1]
    ano_atual = tz_now.year
    anos_disponiveis = range(ano_atual - 5, ano_atual + 6)

    context = {
        "ano": ano,
        "mes": mes,
        "nome_mes": nome_mes,
        "meses": meses,
        "anos_disponiveis": anos_disponiveis,

        # grade pronta para renderizar
        "weeks": weeks_enriched,

        # navegação
        "mes_anterior": mes_anterior,
        "ano_anterior": ano_anterior,
        "mes_seguinte": mes_seguinte,
        "ano_seguinte": ano_seguinte,
    }
    return render(request, "calendario/calendario_mensal.html", context)