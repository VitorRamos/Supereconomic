from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from models import *
from forms import *

def index(request):
    if request.method == "POST" and "logar" in request.POST:
        return login(request)
    elif request.method == "POST" and 'sair' in request.POST:
        auth.logout(request)
        return HttpResponseRedirect('/')
    return render(request, 'home.html')

def login(request):
    avisos= []
    if request.method == "POST" and 'voltar' in request.POST:
        return HttpResponseRedirect('/')

    elif request.method == "POST" and ('logar' in request.POST or 'cadastrar' in request.POST):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('nome'),
                                     password=form.cleaned_data.get('senha'))
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    avisos.append("Essa conta foi desativada.")
            else:
                avisos.append("Senha ou usuario incorretos.")
                #return HttpResponseRedirect('/cadastro')
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

    return render(request, 'login.html', {'form': form, 'avisos': avisos})


def cadastro(request):
    avisos = []

    if request.method == "POST" and 'logar' in request.POST:
        return login(request)

    elif request.method == "POST" and 'voltar' in request.POST:
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
                avisos.append("Cadastrado Com Sucesso")
                #form= CadastroForm() limpa formulario
                return login(request)

            else:
                avisos.append("Usuario ja existe")

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

    return render(request, 'cadastro.html', {'form': form, 'clientes': auth.models.User.objects.all(),
                                             'avisos': avisos})


def favoritos(request):
    if not request.user.groups.filter(name="Clientes").exists():
        return HttpResponseRedirect('/')
    return render(request, 'favoritos.html')

def produtos(request):
    if not request.user.groups.filter(name="Donos").exists():
        return HttpResponseRedirect('/')

    avisos= []
    if request.method == "POST" and 'cadastrarProd' in request.POST:
        form = CadastroProd(request.POST)

        if form.is_valid():
            produto = Produto()
            produto.nome = form.cleaned_data.get('nome')
            produto.marca = form.cleaned_data.get('marca')
            produto.save()

        else:
            avisos.append("Produto Invalido")

    else:
        form = CadastroProd()

    return render(request, 'produtos.html', {'form':form, 'avisos':avisos,
                                             'produtos':Produto.objects.all()})

def sobre(request):
    if request.method == "POST" and "logar" in request.POST:
        return login(request)
    return render(request, 'sobre.html')