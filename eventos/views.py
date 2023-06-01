from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
from .models import Evento
import csv
from secrets import token_urlsafe
import os
from django.conf import settings

@login_required(login_url='/auth/login')
def novo_evento(request):
    if request.method == "GET":
        return render(request, 'novo_evento.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')

        logo = request.FILES.get('logo')

        evento = Evento(
            criador=request.user,
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            carga_horaria=carga_horaria,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
            logo=logo,
        )

        evento.save()
        messages.add_message(request, constants.SUCCESS, 'Evento cadastrado com sucesso!')
        return redirect('/eventos/gerenciar_evento')

@login_required(login_url='/auth/login')
def buscar_evento(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        eventos = Evento.objects.all()
        if nome:
            eventos = eventos.filter(nome__contains=nome)

        return render(request, 'buscar_evento.html', {'eventos': eventos})

@login_required(login_url='/auth/login')
def gerenciar_evento(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        eventos = Evento.objects.filter(criador=request.user)
        if nome:
            eventos = eventos.filter(nome__contains=nome)

        return render(request, 'gerenciar_evento.html', {'eventos': eventos})

@login_required(login_url='/auth/login')
def inscrever_evento(request, id):
    evento = get_object_or_404(Evento, id=id)    
    if request.method == "GET":
        return render(request, "inscrever_evento.html", {'evento': evento})
    elif request.method == "POST":
        #TODO: validar se o usuaria já está no evento
        
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, constants.SUCCESS, 'Pronto! Sua inscrição já está garantida.')
        return redirect(reverse('inscrever_evento', kwargs={'id': id}))

@login_required(login_url='/auth/login')
def participantes_evento(request, id):
    evento = get_object_or_404(Evento, id=id)

    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu!')

    if request.method == "GET":
        participantes = evento.participantes.all()
        return render(request, 'participantes_evento.html', {'evento': evento, 'participantes': participantes})

@login_required(login_url='/auth/login')
def gerar_csv(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu!')

    participantes = evento.participantes.all()

    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    with open(path, 'w') as arq:
        writer = csv.writer(arq, delimiter=",")
        for participante in participantes:
            x=(participante.username, participante.email)
            writer.writerow(x)

    return redirect(f'/media/{token}')
    