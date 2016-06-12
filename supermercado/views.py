from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.decorators import user_passes_test

from forms import LoginForm, CadastroForm, CadastroDono, CadastroProd
from models import Dono, Supermercado, Favorito, Possui, Produto
from supermercado.models import Carrinho

# from django.db.models import Sum

def index(request):
    if request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        return render(request, 'index.html')


@user_passes_test(lambda user: user.is_authenticated() == False)
def login(request):
    avisos = []

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


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@user_passes_test(lambda user: user.is_authenticated() == False)
def cadastro(request):
    avisos = []

    if request.method == 'POST' and 'cadastrar' in request.POST:
        form = CadastroForm(request.POST)

        if form.is_valid():
            if not auth.models.User.objects.filter(username=form.cleaned_data.get('nome')).exists():
                grupo = auth.models.Group.objects.get_or_create(name='Clientes')[0]
                user = auth.models.User.objects.create_user(form.cleaned_data.get('nome'),'emal',
                                                            form.cleaned_data.get('senha'))
                user.groups.add(grupo)
                user.save()
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


@login_required
@permission_required('is_superuser')
def cadastroDono(request):
    avisos_sucesso = []
    avisos_erro = []

    if request.method == 'POST' and 'deletar' in request.POST:
        donoDeletar = Dono.objects.filter(id=request.POST.get('deletar'))[0]
        auth.models.User.objects.filter(id=donoDeletar.idEmpresario.id).delete()
        if Dono.objects.filter(idSupermercado=donoDeletar.idSupermercado.idSupermercado).count() == 0:
            Produto.objects.filter(idProduto__in=
            Possui.objects.filter(idSupermercado=donoDeletar.idSupermercado).values_list('idProduto')).delete()
            Supermercado.objects.filter(idSupermercado=donoDeletar.idSupermercado.idSupermercado).delete()
        donoDeletar.delete()

    if request.method == 'POST' and 'cadastrar' in request.POST:
        form = CadastroDono(request.POST)
        if form.is_valid():
            if not auth.models.User.objects.filter(username=form.cleaned_data.get('nome')).exists():
                grupo = auth.models.Group.objects.get_or_create(name='Donos')[0]
                user = auth.models.User.objects.create_user(form.cleaned_data.get('nome'),'emal',
                                                            form.cleaned_data.get('senha'))
                user.groups.add(grupo)
                user.save()
                supermercado= Supermercado.objects.get_or_create(
                               nome=form.cleaned_data.get('nomeSupermercado'),
                               localizacao=form.cleaned_data.get('localizacao'))[0]

                dono = Dono(idEmpresario=user,
                            idSupermercado=supermercado,
                            CNPJ=form.cleaned_data.get('CNPJ'))
                dono.save()

                form = CadastroDono()
                avisos_sucesso.append('Cadastrado Com Sucesso')
                return HttpResponseRedirect('/cadastroDono')
            else:
                avisos_erro.append('Usuario ja existe')
        else:
            avisos_erro.append('Erro Formulario')
    else:
        form = CadastroDono()
    return render(request, 'cadastroDono.html',
                  {'form': form, 'avisos_erro': avisos_erro, 'avisos_sucesso': avisos_sucesso, 'donos':Dono.objects.all()})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Donos').exists() == True)
def produtos(request):
    avisos = []
    dono = Dono.objects.filter(idEmpresario=request.user.id)[0]
    produtos = Possui.objects.filter(idSupermercado=dono.idSupermercado)

    if request.method == 'POST' and 'deletar' in request.POST:
        if Produto.objects.filter(idProduto__in=request.POST.getlist('produtosDeletar')).exists():
            Produto.objects.filter(idProduto__in=request.POST.getlist('produtosDeletar')).delete()
        else:
            avisos.append('Nenhum Produto Selecionado')

    if request.method == 'POST' and 'cadastrarProd' in request.POST:
        form = CadastroProd(request.POST)

        if form.is_valid():
            produto = Produto(nome=form.cleaned_data.get('nome'),
                              marca=form.cleaned_data.get('marca'),
                              tipo=request.POST.getlist('tipo'))
            produto.save()
            possui = Possui(idProduto=produto,
                            idSupermercado=dono.idSupermercado,
                            preco=form.cleaned_data.get('preco'),
                            quantidade=form.cleaned_data.get('quantidade'))
            possui.save()
            form = CadastroProd()
            return HttpResponseRedirect('/produtos')
    else:
        form = CadastroProd()

    return render(request, 'produtos.html', {'form': form, 'avisos': avisos,
                                             'produtos': produtos.order_by("idProduto__nome")})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Clientes').exists() == True)
def favoritos(request):
    if request.method == 'POST' and 'deletar' in request.POST:
        Favorito.objects.filter(idProduto=request.POST.get('deletar')).delete()

    dadosProd = Possui.objects.filter(idProduto__in=Favorito.objects.filter(
                                                    idCliente=request.user).values_list('idProduto'))
    return render(request, 'favoritos.html', {'prodFavorito': dadosProd})

def carrinho(request):
    if request.method == 'POST' and 'deletar' in request.POST:
        Carrinho.objects.filter(idProduto=request.POST.get('deletar')).delete()

    dadosProd = Possui.objects.filter(idProduto__in=Carrinho.objects.filter(
        idCliente=request.user).values_list('idProduto'))
    TotalCarrinho = 0
    if request.method == 'POST' and 'calcular' in request.POST:
        qnt = map(float,request.POST.getlist('quantidade'))
        prods = Possui.objects.filter(idProduto__in=Carrinho.objects.all().values_list('idProduto'))
        for x in range(0, Carrinho.objects.all().count()):
            TotalCarrinho= TotalCarrinho+prods[x].preco*qnt[x]
        # TotalCarrinho= Possui.objects.filter(
        # idProduto__in=Carrinho.objects.all().values_list('idProduto')).aggregate(total=Sum('preco')).get('total')
    return render(request, 'carrinho.html', {'prodCarrinho': dadosProd, 'TotalCarrinho':TotalCarrinho})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Clientes').exists() == True)
def pesquisa(request):
    pesquisas = []
    aviso_sucess = []
    aviso_error = []

    if request.method == 'GET' and 'buscaSimples' in request.GET:
        pesquisas = Possui.objects.filter(idProduto__in=Produto.objects.filter(
        nome__icontains=request.GET.get('buscaNome'))).order_by("idProduto__nome")

    if request.method == 'POST' and 'favoritar' in request.POST:
        favoritos = request.POST.getlist('prodSel')
        #TODO aviso nada selecionado
        for id in favoritos:
            produtoFavorito = Produto.objects.filter(idProduto=id)[0]
            if not Favorito.objects.filter(idProduto=produtoFavorito, idCliente=request.user).exists():
                favorito = Favorito(idProduto=produtoFavorito, idCliente=request.user)
                favorito.save()
                aviso_sucess.append(produtoFavorito.nome + ' cadastrado com sucesso ')
                #TODO reenvio de formulario
                # return HttpResponseRedirect('/pesquisa')
            else:
                aviso_error.append('Esse produto ja esta nos seus favoritos')

    if request.method == 'POST' and 'carrinho' in request.POST:
        carrinhoProd = request.POST.getlist('prodSel')
        # TODO aviso nada selecionado
        for id in carrinhoProd:
            produtoCarrinho = Produto.objects.filter(idProduto=id)[0]
            if not Carrinho.objects.filter(idProduto=produtoCarrinho, idCliente=request.user).exists():
                carrinho_ = Carrinho(idProduto=produtoCarrinho, idCliente=request.user)
                carrinho_.save()
                aviso_sucess.append(produtoCarrinho.nome + ' colocado no carrinho')
                # TODO reenvio de formulario
                # return HttpResponseRedirect('/pesquisa')
            else:
                aviso_error.append('ja esta no seu carrinho')

    return render(request, 'pesquisa.html',
                  {'pesquisa': pesquisas, 'aviso_sucess': aviso_sucess, 'aviso_error': aviso_error,
                   'favoritos': Possui.objects.filter(idProduto__in=Favorito.objects.filter(idCliente=request.user.id).values('idProduto'))})


def sobre(request):
    return render(request, 'sobre.html')