from django.shortcuts import render
from models import *
from forms import *

def index(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    if request.method == "POST" and 'voltar' in request.POST:
        return render(request, 'home.html')

    elif request.method == "POST" and 'submit' in request.POST:
        form = ClienteForm(request.POST)

        if form.is_valid():
            user = Usuario()
            cliente = Cliente()
            user.nome = form.cleaned_data.get('nome')
            user.senha = form.cleaned_data.get('senha')
            user.save()
            cliente.idCliente = user
            cliente.CPF = form.cleaned_data.get('CPF')
            cliente.save()
    else:
        form = ClienteForm()
    return render(request, 'cadastro.html', {'form': form, 'clientes': Cliente.objects.all()})

def sobre(request):
    return render(request, 'sobre.html')