# ARQUIVO CORRIGIDO E FINAL: novosite/usuarios/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib import messages
from django.contrib.messages import constants
from .models import Produto

# --- Views de Autenticação e Páginas Básicas ---

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(request, username=username, password=senha)
        if user:
            login_django(request, user)
            messages.add_message(request, constants.SUCCESS, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            messages.add_message(request, constants.ERROR, 'E-mail ou senha inválidos!')
            return redirect('login')
    return render(request, 'usuarios/login.html')

@login_required(login_url='/login/')
def logout(request):
    logout_django(request)
    messages.add_message(request, constants.INFO, 'Você saiu do sistema.')
    return redirect('login')

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        first_name = request.POST.get('nome')
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.WARNING, 'Usuário já existente!')
            return redirect('cadastro')
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
        user.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso! Faça seu login.')
        return redirect('login')
    return render(request, 'usuarios/cadastro.html')

@login_required(login_url='/login/')
def home(request):
    return render(request, 'usuarios/home.html')

# --- LÓGICA DO GESTOR DE ESTOQUE (CRUD) ---

@login_required(login_url='/login/')
def lancar(request):
    if request.method == "POST":
        nome = request.POST.get('nome_produto')
        qtd = request.POST.get('quantidade')
        preco_custo = request.POST.get('preco_custo')
        preco_venda = request.POST.get('preco_venda')
        fornecedor = request.POST.get('fornecedor')
        if not all([nome, qtd, preco_custo, preco_venda]):
            messages.add_message(request, constants.ERROR, 'Todos os campos com * são obrigatórios.')
            return redirect('lancar')
        produto = Produto(
            usuario=request.user, nome_produto=nome, quantidade=qtd,
            preco_custo=preco_custo, preco_venda=preco_venda, fornecedor=fornecedor
        )
        produto.save()
        messages.add_message(request, constants.SUCCESS, 'Produto cadastrado com sucesso!')
        return redirect('lancar')
    return render(request, 'usuarios/lancar.html')

@login_required(login_url='/login/')
def visualizar(request):
    produtos = Produto.objects.filter(usuario=request.user)
    filtro_nome = request.GET.get('filtro_nome')
    if filtro_nome:
        produtos = produtos.filter(nome_produto__icontains=filtro_nome)
    return render(request, 'usuarios/visualizar.html', {'produtos': produtos})

@login_required(login_url='/login/')
def editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if not produto.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para editar este item.')
        return redirect('visualizar')
    if request.method == 'POST':
        produto.nome_produto = request.POST.get('nome_produto')
        produto.quantidade = request.POST.get('quantidade')
        produto.preco_custo = request.POST.get('preco_custo')
        produto.preco_venda = request.POST.get('preco_venda')
        produto.fornecedor = request.POST.get('fornecedor')
        produto.save()
        messages.add_message(request, constants.SUCCESS, 'Produto atualizado com sucesso!')
        return redirect('visualizar')
    return render(request, 'usuarios/editar.html', {'produto': produto})

@login_required(login_url='/login/')
def excluir(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if not produto.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para acessar esta página.')
        return redirect('visualizar')
    return render(request, 'usuarios/excluir.html', {'produto': produto})

@login_required(login_url='/login/')
def excluir_final(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if not produto.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para excluir este item.')
        return redirect('visualizar')
    produto.delete()
    messages.add_message(request, constants.SUCCESS, 'Produto excluído com sucesso!')
    return redirect('visualizar')

# --- Páginas Estáticas (Sobre e Contato) ---

def sobre(request):
    return render(request, 'usuarios/sobre.html')

def contato(request):
    return render(request, 'usuarios/contato.html')