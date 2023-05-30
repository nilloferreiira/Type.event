from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

    if not (senha == confirmar_senha):
        messages.add_message(request, constants.ERROR, 'As senhas não são iguais')
        return redirect(reverse('cadastro'))
    
    #TODO validar força senha

    user = User.objects.filter(username=username)

    if user.exists():
        messages.add_message(request, constants.ERROR, 'Usuário já cadastrado no sistema!')
        return redirect(reverse('cadastro'))

    user = User.objects.create_user(username=username, email=email, password=senha)
    user.save()
    messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
    return redirect(reverse('login'))

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
   
    elif request.method == "POST":
        username = request.POST.get('username')
        senha =  request.POST.get('senha')
        print(username, senha)
        user = auth.authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, constants.ERROR, 'username ou senha incorretos')
            return redirect(reverse('login'))

        auth.login(request, user)
        return redirect('/eventos/novo_evento')