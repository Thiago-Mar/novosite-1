from django.contrib import admin
from .models import Produto  # Corrigido para importar Produto

# Registra o modelo Produto na área de administração
admin.site.register(Produto)