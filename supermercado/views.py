from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from forms import LoginForm, CadastroForm, CadastroDono, CadastroProd
from models import Dono, Supermercado, Favorito, Possui, Produto


def index(request):
    return render(request, 'home.html')


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    avisos= []

    if request.method == 'GET' and ('logar' in request.GET or 'logarGlobal' in request.GET):
        form = LoginForm(request.GET)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('nome'),
                                     password=form.cleaned_data.get('senha'))
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    avisos.append('Essa conta foi desativada.')
            else:
                avisos.append('Senha ou usuario incorretos.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'avisos': avisos})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def cadastro(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    avisos = []

    if request.method == 'POST' and 'cadastrar' in request.POST:
        form = CadastroForm(request.POST)

        if form.is_valid():
            if auth.models.User.objects.filter(username=form.cleaned_data.get('nome')).count() == 0:
                grupo = auth.models.Group.objects.get(name='Clientes')
                user = auth.models.User.objects.create_user(form.cleaned_data.get('nome'),
                                                            'emal', form.cleaned_data.get('senha'))
                user.groups.add(grupo)
                user.save()
                # avisos.append('Cadastrado Com Sucesso')
                user = auth.authenticate(username=form.cleaned_data.get('nome'),
                                         password=form.cleaned_data.get('senha'))
                auth.login(request, user)
                return HttpResponseRedirect('/')

            else:
                avisos.append('Usuario ja existe')
                form = CadastroForm()
    else:
        form = CadastroForm()

    return render(request, "cadastro.html", {'form': form, 'avisos': avisos})

def cadastroDono(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    avisos_sucesso= []
    avisos_erro= []
    if request.method == 'POST' and 'cadastrar' in request.POST:
        form = CadastroDono(request.POST)
        if form.is_valid():
            if auth.models.User.objects.filter(username=form.cleaned_data.get('nome')).exists():
                avisos_erro.append('Usuario ja existe')
            else:
                grupo = auth.models.Group.objects.get(name='Donos')
                user = auth.models.User.objects.create_user(form.cleaned_data.get('nome'),
                                                            'emal',
                                                            form.cleaned_data.get('senha'))
                user.groups.add(grupo)
                user.save()
                supermercado= Supermercado.objects.filter(nome=form.cleaned_data.get('nomeSupermercado'),
                                               localizacao=form.cleaned_data.get('localizacao'))[0]
                if not supermercado.exists():
                    supermercado = Supermercado(nome= form.cleaned_data.get('nomeSupermercado'),
                                            localizacao= form.cleaned_data.get('localizacao'))
                    supermercado.save()

                dono = Dono(idEmpresario= user,
                            idSupermercado= supermercado,
                            CNPJ=form.cleaned_data.get('CNPJ'))
                dono.save()

                form = CadastroDono()
                avisos_sucesso.append('Cadastrado Com Sucesso')
        else:
            avisos_erro.append('Erro Formulario')
    else:
        form= CadastroDono()
    return render(request, 'cadastroDono.html', {'form':form, 'avisos_erro':avisos_erro, 'avisos_sucesso':avisos_sucesso})



def produtos(request):
    if not request.user.groups.filter(name='Donos').exists():
        return HttpResponseRedirect('/')

    avisos = []
    if request.method == 'POST' and 'cadastrarProd' in request.POST:
        form = CadastroProd(request.POST)

        if form.is_valid():
            dono = Dono.objects.filter(idEmpresario=request.user.id)[0]

            produto = Produto(nome=form.cleaned_data.get('nome'),
                              marca=form.cleaned_data.get('marca'))
            produto.save()
            possui = Possui(idProduto= produto,
                            idSupermercado=dono.idSupermercado,
                            preco=form.cleaned_data.get('preco'),
                            quantidade= form.cleaned_data.get('quantidade'))
            possui.save()
            form = CadastroProd()
        else:
            avisos.append('Produto Invalido')
    else:
        form = CadastroProd()

    dono = Dono.objects.filter(idEmpresario=request.user.id)[0]
    produtos = Possui.objects.filter(idSupermercado=dono.idSupermercado)
    return render(request, 'produtos.html', {'form': form, 'avisos': avisos,
                                             'produtos': produtos})


def favoritos(request):
    if not request.user.groups.filter(name='Clientes').exists():
        return HttpResponseRedirect('/')

    prodFavorito = Favorito.objects.filter(idCliente=request.user).values_list('idProduto')
    dadosProd = Possui.objects.filter(idProduto__in=prodFavorito)

    return render(request, 'favoritos.html', {'prodFavorito':dadosProd})


def pesquisa(request):
    if not request.user.groups.filter(name='Clientes').exists():
        return HttpResponseRedirect("/")

    pesquisas = []
    if request.method == 'GET' and 'buscaSimples' in request.GET:
        pesAux = Produto.objects.filter(nome__icontains = request.GET.get('buscaNome'))
        pesquisas = Possui.objects.filter(idProduto__in = pesAux)

    aviso_sucess = []
    aviso_error = []

    if request.method == 'POST' and 'favoritar' in request.POST:
        favoritos = request.POST.getlist('favoritos')
        for id in favoritos:
            produtoFavorito = Produto.objects.filter(idProduto=id)[0]
            if not Favorito.objects.filter(idProduto=produtoFavorito, idCliente=request.user).exists() :
                favorito = Favorito(idProduto=produtoFavorito, idCliente=request.user)
                favorito.save()
                aviso_sucess.append(produtoFavorito.nome+' cadastrado com sucesso ' )
            else:
                aviso_error.append('Esse produto ja esta nos seus favoritos')

    return render(request, 'pesquisa.html', {'pesquisa':pesquisas, 'aviso_sucess':aviso_sucess, 'aviso_error':aviso_error})


def sobre(request):
    return render(request, 'sobre.html')