# ARQUIVO CORRETO E FINAL: novosite/usuarios/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # A URL raiz '' agora aponta DIRETAMENTE para a página de login.
    # Esta é a primeira página que um usuário não autenticado verá.
    path('', views.login, name='login'),
    
    # As outras URLs de autenticação
    path('logout/', views.logout, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    
    # A 'home' agora tem seu próprio caminho e é a página principal APÓS o login.
    path('home/', views.home, name='home'),
    
    # URLs do sistema de estoque
    path('lancar/', views.lancar, name='lancar'),
    path('visualizar/', views.visualizar, name='visualizar'),
    path('editar/<int:pk>/', views.editar, name='editar'),
    path('excluir/<int:pk>/', views.excluir, name='excluir'),
    path('excluir_final/<int:pk>/', views.excluir_final, name='excluir_final'),
    
    # URLs das páginas extras
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
]