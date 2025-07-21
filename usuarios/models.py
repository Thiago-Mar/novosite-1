from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_produto = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.CharField(max_length=100, blank=True)
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_produto} - Qtd: {self.quantidade}"
