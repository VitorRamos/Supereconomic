from django.shortcuts import render
from django.contrib import auth
from models import *
from forms import *


def index(request):
    if request.method == "POST" and 'sair' in request.POST:
        auth.logout(request)
    return render(request, 'home.html')


def login(request):
    if request.method == "POST" and 'voltar' in request.POST:
        return render(request, 'home.html')

    elif request.method == "POST" and 'logar' in request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('nome'),
                                     password=form.cleaned_data.get('senha'))

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                print("The username and password were incorrect.")
        # sem usar django
        #if form.is_valid():
            # user = Usuario()
            # user.nome = form.cleaned_data.get('nome')
            # user.senha = form.cleaned_data.get('senha')
            # data = Usuario.objects.filter(nome=user.nome, senha=user.senha)
            # if data.count() == 0:
            #     print("Usuario nao cadastrado")
            # for x in data:
            #     print(x.senha)

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def cadastro(request):
    if request.method == "POST" and 'voltar' in request.POST:
        return render(request, 'home.html')

    elif request.method == "POST" and 'cadastrar' in request.POST:
        form = CadastroForm(request.POST)

        if form.is_valid():
            if auth.models.User.objects.filter(username=form.cleaned_data.get('nome')).count() == 0:
                grupo = auth.models.Group.objects.get(name='Clientes')
                user = auth.models.User.objects.create_user(form.cleaned_data.get('nome'),
                                                            'emal', form.cleaned_data.get('senha'))
                user.groups.add(grupo)
                user.save()
            else:
                print("Usuario ja existe")

        #if form.is_valid():
        #sem usar django
        # user = Usuario()
        # cliente = Cliente()
        # user.nome = form.cleaned_data.get('nome')
        # user.senha = form.cleaned_data.get('senha')
        # user.save()
        # cliente.idCliente = user
        # cliente.CPF = form.cleaned_data.get('CPF')
        # cliente.save()
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form, 'clientes': auth.models.User.objects.all()})


def sobre(request):
    return render(request, 'sobre.html')