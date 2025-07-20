# novosite/usuarios/models.py

from django.db import models
from django.contrib.auth.models import User

# RENOMEIE a classe de 'Nota' para 'Produto'
class Produto(models.Model):
    # MANTENHA o usuário, ele indica quem cadastrou o produto
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # ALTERE os campos para refletir um produto
    nome_produto = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.CharField(max_length=100, blank=True) # Exemplo de campo novo
    data_cadastro = models.DateField(auto_now_add=True)

    # ALTERE o __str__ para facilitar a identificação no admin
    def __str__(self):
        return f"{self.nome_produto} - Qtd: {self.quantidade}"