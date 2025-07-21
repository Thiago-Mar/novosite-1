from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django, logout as logout_django
from .models import Produto
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import render, redirect


def login(request):
    if request.method == "GET":
        return render(request, 'usuarios/login.html')
    else:
        username = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(username = username, password = senha)

        if user:
            login_django(request, user)
            return render(request, 'usuarios/home.html')
        else:
            return HttpResponse('E-mail ou senha inválidos!')

def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return render(request, 'usuarios/login.html')
    else:
        return HttpResponse("Você não acessou sua conta ainda!")

def cadastro(request):
    if request.method == "GET":
        return render(request, 'usuarios/cadastro.html')
    else:
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        first_name = request.POST.get('nome')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse("Usuário já existente!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()

            return render(request, 'usuarios/login.html')
        
def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html')
    else:
        return HttpResponse("Faça o login para acessar!")


def lancar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'usuarios/lancar.html')
        else:
            return HttpResponse("Faça o login para acessar!")

    elif request.method == "POST":
        nome = request.POST.get('nome_produto')
        qtd = request.POST.get('quantidade')
        preco_custo = request.POST.get('preco_custo')
        preco_venda = request.POST.get('preco_venda')
        fornecedor = request.POST.get('fornecedor')

        if not all([nome, qtd, preco_custo, preco_venda]):
            messages.add_message(request, constants.ERROR, 'Todos os campos com * são obrigatórios.')
            return redirect('lancar')

        produto_existente = Produto.objects.filter(nome_produto=nome).first()
        if produto_existente:
            messages.add_message(request, constants.ERROR, 'Produto já cadastrado.')
            return redirect('lancar')

        produto = Produto(
            usuario=request.user,
            nome_produto=nome,
            quantidade=int(qtd),
            preco_custo=preco_custo,
            preco_venda=preco_venda,
            fornecedor=fornecedor
        )
        produto.save()

        messages.add_message(request, constants.SUCCESS, 'Produto cadastrado com sucesso!')
        return redirect('lancar')

def alterar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_produtos = Produto.objects.all()
            dicionario_produtos = {'lista_produtos':lista_produtos}
            return render(request, 'usuarios/alterar.html', dicionario_produtos)
        else:
            return HttpResponse("Faça o login para acessar!")

from django.http import HttpResponse
from django.shortcuts import render
from .models import Produto

from django.shortcuts import render
from .models import Produto
from django.http import HttpResponse

def visualizar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_produtos = Produto.objects.all() 
            dicionario_dados = {'lista_produtos': lista_produtos}
            return render(request, 'usuarios/visualizar.html', dicionario_dados)
        else:
            return HttpResponse("Faça o login para acessar!") 
    else: # request.method == "POST"
        # Agora o nome do campo no POST será 'nome_produto', correspondendo ao HTML
        nome_produto_filtro = request.POST.get('nome_produto') 
        
        if nome_produto_filtro == "Todos os produtos":
            lista_produtos = Produto.objects.all()
            dicionario_produtos = {'lista_produtos': lista_produtos}
        else:
            # Garante que o filtro usa o valor correto do POST
            lista_produtos = Produto.objects.filter(nome_produto=nome_produto_filtro) 
            dicionario_produtos = {'lista_produtos': lista_produtos}
            
        return render(request, 'usuarios/visualizar.html', dicionario_produtos)
        
def excluir_verificacao(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_produtos = Produto.objects.get(pk=pk) 
            dicionario_produtos = {'lista_produtos':lista_produtos}     
            return render(request, 'usuarios/excluir.html', dicionario_produtos) 
        else:
            return HttpResponse("Faça o login para acessar!")      

def excluir(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            produto_selecionado = Produto.objects.get(pk=pk)
            produto_selecionado.delete()
            return HttpResponseRedirect(reverse('alterar'))
        else:
            return HttpResponse("Faça o login para acessar!")

def editar_verificacao(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_produtos = Produto.objects.get(pk=pk)
            dicionario_produtos = {'lista_produtos':lista_produtos}
            return render(request, 'usuarios/editar.html', dicionario_produtos)
        else:
            return HttpResponse("Faça o login para acessar!")

def editar(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse("Faça o login para acessar!")

    produto = Produto.objects.get(pk=pk)

    if request.method == "POST":
        nome = request.POST.get('nome_produto')
        qtd = request.POST.get('quantidade')
        preco_custo = request.POST.get('preco_custo')
        preco_venda = request.POST.get('preco_venda')
        fornecedor = request.POST.get('fornecedor')

        # Atualiza o produto
        produto.nome_produto = nome
        produto.quantidade = qtd
        produto.preco_custo = preco_custo
        produto.preco_venda = preco_venda
        produto.fornecedor = fornecedor
        produto.save()

        messages.add_message(request, constants.SUCCESS, 'Produto atualizado com sucesso!')
        return HttpResponseRedirect(reverse('alterar'))

    # Se for GET, renderiza a tela de edição
    return render(request, 'usuarios/editar.html', {'lista_produtos': produto})




